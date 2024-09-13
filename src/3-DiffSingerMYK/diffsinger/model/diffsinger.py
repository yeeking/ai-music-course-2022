import os
import json

import torch
import torch.nn as nn
import torch.nn.functional as F

from .blocks import LinearNorm
from .modules import TextEncoder, VarianceAdaptor, AuxDecoder
from .diffusion import GaussianDiffusion
from utils.tools import get_mask_from_lengths


class DiffSinger(nn.Module):
    """ DiffSinger """

    def __init__(self, preprocess_config, model_config, train_config):
        super(DiffSinger, self).__init__()
        self.model_config = model_config

        self.text_encoder = TextEncoder(model_config)
        self.variance_adaptor = VarianceAdaptor(preprocess_config, model_config)
        self.aux_decoder = AuxDecoder(model_config)
        self.diffusion = GaussianDiffusion(preprocess_config, model_config, train_config)

        self.speaker_emb = None
        if model_config["multi_speaker"]:
            with open(
                os.path.join(
                    preprocess_config["path"]["preprocessed_path"], "speakers.json"
                ),
                "r",
            ) as f:
                n_speaker = len(json.load(f))
            self.speaker_emb = nn.Embedding(
                n_speaker,
                model_config["transformer"]["encoder_hidden"],
            )

    def forward(
        self,
        speakers,
        texts,
        src_lens,
        max_src_len,
        mels=None,
        mel_lens=None,
        max_mel_len=None,
        p_targets=None,
        e_targets=None,
        d_targets=None,
        p_control=1.0,
        e_control=1.0,
        d_control=1.0,
    ):
        src_masks = get_mask_from_lengths(src_lens, max_src_len)
        mel_masks = (
            get_mask_from_lengths(mel_lens, max_mel_len)
            if mel_lens is not None
            else None
        )

        output = self.text_encoder(texts, src_masks)
        print("diffsinger.py::forward  src lens", src_lens, " text encoded output shape ", output.shape)
        if self.speaker_emb is not None:
            output = output + self.speaker_emb(speakers).unsqueeze(1).expand(
                -1, max_src_len, -1
            )

        (
            output,
            p_predictions,
            e_predictions,
            log_d_predictions,
            d_rounded,
            mel_lens,
            mel_masks,
        ) = self.variance_adaptor(
            output,
            src_masks,
            mel_masks,
            max_mel_len,
            p_targets,
            e_targets,
            d_targets,
            p_control,
            e_control,
            d_control,
        )

        (
            output,
            epsilon_predictions,
            noise_loss,
            diffusion_step,
        ) = self.diffusion(
            mels,
            output,
            mel_masks,
        )

        return (
            output,
            epsilon_predictions,
            noise_loss,
            diffusion_step,
            p_predictions,
            e_predictions,
            log_d_predictions,
            d_rounded,
            src_masks,
            mel_masks,
            src_lens,
            mel_lens,
        )
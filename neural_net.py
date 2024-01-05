import torch
import torch.nn as nn
import numpy as np


class YourNetwork(nn.Module):
    def __init__(self, obs_size=42, hidden_size1=10,
                 hidden_size2=5, output_size=7):
        self._total_weights = (
            obs_size * hidden_size1
            + hidden_size1
            + hidden_size1 * hidden_size2
            + hidden_size2
            + hidden_size2 * output_size
            + output_size
        )
        super().__init__()
        self.hidden_linear1 = nn.Linear(obs_size, hidden_size1).float()
        self.hidden_linear2 = nn.Linear(hidden_size1, hidden_size2).float()
        self.output_linear = nn.Linear(hidden_size2, output_size).float()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def num_params(self):
        return self._total_weights

    def forward(self, obs: np.array) -> int:
        obs = torch.from_numpy(obs).float()
        hidden_t1 = self.hidden_linear1(obs)
        activated_t1 = torch.tanh(hidden_t1)
        hidden_t2 = self.hidden_linear2(activated_t1)
        activated_t2 = torch.tanh(hidden_t2)
        output_t = self.output_linear(activated_t2)
        output_softmax = torch.nn.functional.softmax(output_t, dim=0)
        output_class = torch.argmax(output_softmax, dim=0)
        return output_class.item()

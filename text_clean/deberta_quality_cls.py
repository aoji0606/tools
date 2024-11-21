import json
import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer, AutoConfig
from huggingface_hub import PyTorchModelHubMixin
from tqdm import tqdm


class QualityModel(nn.Module, PyTorchModelHubMixin):
    def __init__(self, config):
        super(QualityModel, self).__init__()
        self.model = AutoModel.from_pretrained(config["base_model"])
        self.dropout = nn.Dropout(config["fc_dropout"])
        self.fc = nn.Linear(self.model.config.hidden_size, len(config["id2label"]))

    def forward(self, input_ids, attention_mask):
        features = self.model(
            input_ids=input_ids, attention_mask=attention_mask
        ).last_hidden_state
        dropped = self.dropout(features)
        outputs = self.fc(dropped)
        return torch.softmax(outputs[:, 0, :], dim=1)


device = "cuda" if torch.cuda.is_available() else "cpu"

# Setup configuration and model
# https://huggingface.co/nvidia/quality-classifier-deberta
print("load model...")
path = "../models/quality-classifier-deberta"
config = AutoConfig.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
model = QualityModel.from_pretrained(path).to(device)
model.eval()

# Prepare and process inputs
print("load data...")
data = json.load(open("openorca.json"))

high_num = 0
mid_num = 0
low_num = 0
err_num = 0
for i in tqdm(data):
    try:
        convs = i["conversations"]
        text_samples = ""
        for conv in convs:
            temp = conv["value"] + '\n'
            text_samples += temp

        inputs = tokenizer(text_samples, return_tensors="pt", padding="longest", truncation=True).to(device)
        outputs = model(inputs["input_ids"], inputs["attention_mask"])
        predicted_classes = torch.argmax(outputs, dim=1)
        predicted_domains = [config.id2label[class_idx.item()] for class_idx in predicted_classes.cpu().numpy()]
        i["quality"] = predicted_domains[0]
    except:
        i["quality"] = "error"
        err_num += 1

    if i["quality"] == "Low":
        print(i["quality"])
        low_num += 1
    elif i["quality"] == "Medium":
        print(" " * 20, i["quality"])
        mid_num += 1
    elif i["quality"] == "High":
        print(" " * 40, i["quality"])
        high_num += 1

print(f"high_num:{high_num}, mid_num:{mid_num}, low_num:{low_num}, err_num:{err_num}")
json.dump(data, open("quality.json", 'w'), indent=2, ensure_ascii=False)

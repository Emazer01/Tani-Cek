"""
Pipeline Pelatihan Model Deep Learning TaniCek AI (TaniCekNet CNN)
Dirancang khusus untuk klasifikasi cepat dan akurat citra penyakit tanaman pangan tropis.
"""

import sys
import time
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "data" / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "val"
MODELS_OUT = BASE_DIR / "models_saved"
MODELS_OUT.mkdir(parents=True, exist_ok=True)

class TaniCekNet(nn.Module):
    """Deep Convolutional Neural Network khusus deteksi patogen tanaman"""
    def __init__(self, num_classes=16):
        super().__init__()
        self.features = nn.Sequential(
            # Blok Konvolusi 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), # 64x64

            # Blok Konvolusi 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), # 32x32

            # Blok Konvolusi 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), # 16x16

            # Blok Konvolusi 4
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)

def train_model(num_epochs=10, batch_size=32, lr=0.001):
    print("=" * 65)
    print("🌾 MEMULAI PELATIHAN MODEL DEEP LEARNING TANICEK-NET")
    print("=" * 65)

    train_transforms = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transforms = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(str(TRAIN_DIR), transform=train_transforms)
    val_dataset = datasets.ImageFolder(str(VAL_DIR), transform=val_transforms)

    classes = train_dataset.classes
    num_classes = len(classes)
    print(f"Total Kelas: {num_classes}")
    print(f"Jumlah Sampel: {len(train_dataset)} training, {len(val_dataset)} validasi")

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    class_mapping = {i: c for i, c in enumerate(classes)}
    with open(MODELS_OUT / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(class_mapping, f, indent=2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Menggunakan perangkat komputasi: {device}")

    model = TaniCekNet(num_classes=num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

    history = {
        "model_name": "TaniCekNet (Deep Convolutional Neural Network)",
        "num_classes": num_classes,
        "classes": classes,
        "total_train_samples": len(train_dataset),
        "total_val_samples": len(val_dataset),
        "epochs": [],
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": []
    }

    best_val_acc = 0.0
    start_time = time.time()

    print("\n--- Proses Pelatihan Berlangsung ---")
    print(f"{'Epoch':<8} | {'Train Loss':<12} | {'Train Acc':<12} | {'Val Loss':<12} | {'Val Acc':<12} | {'Waktu'}")
    print("-" * 75)

    for epoch in range(1, num_epochs + 1):
        epoch_start = time.time()

        # Training Phase
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += (preds == labels).sum().item()
            total_train += labels.size(0)

        scheduler.step()

        train_loss = running_loss / total_train
        train_acc = (correct_train / total_train) * 100.0

        # Validation Phase
        model.eval()
        val_running_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for val_images, val_labels in val_loader:
                val_images = val_images.to(device)
                val_labels = val_labels.to(device)

                val_outputs = model(val_images)
                v_loss = criterion(val_outputs, val_labels)

                val_running_loss += v_loss.item() * val_images.size(0)
                _, v_preds = torch.max(val_outputs, 1)
                correct_val += (v_preds == val_labels).sum().item()
                total_val += val_labels.size(0)

        val_loss = val_running_loss / total_val
        val_acc = (correct_val / total_val) * 100.0
        epoch_duration = time.time() - epoch_start

        history["epochs"].append(epoch)
        history["train_loss"].append(round(train_loss, 4))
        history["train_acc"].append(round(train_acc, 2))
        history["val_loss"].append(round(val_loss, 4))
        history["val_acc"].append(round(val_acc, 2))

        print(f"{epoch:<8} | {train_loss:<12.4f} | {train_acc:<11.2f}% | {val_loss:<12.4f} | {val_acc:<11.2f}% | {epoch_duration:.1f}s")

        if val_acc >= best_val_acc:
            best_val_acc = val_acc
            checkpoint_path = MODELS_OUT / "tanicek_vision_model.pth"
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "val_acc": val_acc,
                "classes": classes
            }, str(checkpoint_path))

    total_duration = time.time() - start_time
    history["final_best_val_acc"] = round(best_val_acc, 2)
    history["training_time_seconds"] = round(total_duration, 1)

    with open(MODELS_OUT / "training_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print("-" * 75)
    print(f"[SELESAI] Pelatihan selesai dalam {total_duration:.1f} detik.")
    print(f"[HASIL] Akurasi Validasi Terbaik: {best_val_acc:.2f}%")
    print(f"[DISIMPAN] Checkpoint Model: {MODELS_OUT / 'tanicek_vision_model.pth'}")
    print("=" * 65)

if __name__ == "__main__":
    train_model(num_epochs=10, batch_size=32, lr=0.001)

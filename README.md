# 🕸️ Script Lanman (Network Protocol Hardener)


<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-2496ED?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Windows_Only-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
</div>

---

### 📋 The Problem (Diagnosis)
In complex legacy ERP environments (Non-Active Directory), Windows 10/11 updates frequently break **Network Discovery**, **Printer Sharing**, and **SMB Authentication**. 

Throughout **1,000+ technical support cases**, the solution was always a specific permutation of Registry Keys involving NTLM, SMB Signing, and RPC levels. Manually editing the Registry (`regedit`) is error-prone and time-consuming for Tier 1 support.

### 🛠️ The Solution (The Tool)
**Script Lanman** is a GUI-based Force Multiplier that encapsulates senior-level troubleshooting knowledge into a single execution. It automates the standardization of communication protocols to ensure legacy systems can "see" each other.

**Key Capabilities:**
* ✅ **NTLMv1 Fallback:** Enables compatibility with legacy NAS/Printers (`LmCompatibilityLevel`).
* ✅ **SMB Optimization:** Disables strict signing to prevent timeouts in unstable networks.
* ✅ **RPC Hardening Fix:** Reverts `RpcAuthnLevelPrivacyEnabled` to allow network printing.
* ✅ **Visual Feedback:** Dark Mode GUI with real-time log of registry changes.

---

### 💻 Technical Implementation

The script utilizes `winreg` for low-level system calls and `customtkinter` for the interface.

**Targeted Registry Hives:**
| Component | Registry Key Modified | Value |
| :--- | :--- | :--- |
| **Legacy Auth** | `HKLM\...\Control\Lsa\LmCompatibilityLevel` | `1` (NTLMv1) |
| **Guest Access** | `HKLM\...\LanmanWorkstation\AllowInsecureGuestAuth` | `1` (Enable) |
| **SMB Signing** | `HKLM\...\LanmanWorkstation\RequireSecuritySignature` | `0` (Disable) |
| **Printer RPC** | `HKLM\...\Control\Print\RpcAuthnLevelPrivacyEnabled` | `0` (Disable) |

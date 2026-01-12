"""
PROJECT: Script Lanman
AUTHOR: Rafael Cavalheiro
DESCRIPTION: 
    GUI Tool to automate Windows Registry modifications for 
    Network Discovery and Legacy SMB/NTLM support.
    Born from 1000+ support cases in ERP environments.
"""

import customtkinter as ctk
import winreg
import ctypes
import sys
import os
import time
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class LanmanTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Script Lanman")
        self.geometry("680x650")
        self.resizable(False, False)

        try:
            self.iconbitmap(resource_path("jacare.ico"))
        except: pass

        # === CABEÇALHO ===
        self.lbl_title = ctk.CTkLabel(self, text="Script Lanman", font=("Roboto", 22, "bold"))
        self.lbl_title.pack(pady=(15, 0))
        
        self.lbl_desc = ctk.CTkLabel(self, text="Automação de Protocolos de Rede e NTLM/SMB", font=("Roboto", 12), text_color="gray")
        self.lbl_desc.pack(pady=(0, 10))

        # === ÁREA DE OPÇÕES (Checkboxes) ===
        self.frame_checks = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_checks.pack(pady=5, padx=20, fill="x")

        self.vars = {
            "blank_logon": ctk.BooleanVar(value=True),
            "enable_ntlmv1": ctk.BooleanVar(value=True),
            "disable_uac": ctk.BooleanVar(value=True),
            "disable_smb_sign": ctk.BooleanVar(value=True),
            "guest_logon": ctk.BooleanVar(value=True),
            "disable_secure_negotiate": ctk.BooleanVar(value=True),
            "rpc_auth_privacy": ctk.BooleanVar(value=True),
        }

        # Checkboxes com fonte moderna
        self.create_check("Configurar logon local com conta em branco", "blank_logon")
        self.create_check("Habilitar LANMAN (NTLMv1 - Legacy Support)", "enable_ntlmv1")
        self.create_check("Desabilitar UAC (Controle de Conta)", "disable_uac")
        self.create_check("Desabilitar assinatura de segurança SMB", "disable_smb_sign")
        self.create_check("Habilitar logon de convidados SMB (Insecure)", "guest_logon")
        self.create_check("Desabilitar negociação segura SMB", "disable_secure_negotiate")
        self.create_check("Aplicar correção RpcAuthnLevelPrivacyEnabled", "rpc_auth_privacy")

        # === TERMINAL DE LOG ===
        self.frame_log = ctk.CTkFrame(self, fg_color="#181818")
        self.frame_log.pack(pady=10, padx=15, fill="both", expand=True)

        self.textbox_log = ctk.CTkTextbox(
            self.frame_log, 
            font=("Roboto Medium", 13), # Fonte moderna
            fg_color="#181818",
            text_color="#E0E0E0",
            activate_scrollbars=True
        )
        self.textbox_log.pack(fill="both", expand=True, padx=10, pady=10)

        # Configuração de Cores (Tags)
        self.textbox_log.tag_config("GREEN", foreground="#00E676")
        self.textbox_log.tag_config("RED", foreground="#FF1744")
        self.textbox_log.tag_config("YELLOW", foreground="#FFEA00")
        self.textbox_log.tag_config("CYAN", foreground="#00B0FF")
        self.textbox_log.tag_config("HEADER", foreground="#FFFFFF")

        self.textbox_log.insert("0.0", "Sistema de configuração pronto.\n")

        # === BOTÃO DE AÇÃO ===
        self.btn_apply = ctk.CTkButton(self, text="APLICAR CONFIGURAÇÕES", command=self.start_thread, height=45, font=("Roboto", 14, "bold"), fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_apply.pack(pady=15, padx=40, fill="x")

    def create_check(self, text, var_key):
        cb = ctk.CTkCheckBox(self.frame_checks, text=text, variable=self.vars[var_key], font=("Roboto", 12), border_width=2)
        cb.pack(anchor="w", pady=3)

    def log(self, msg, type="INFO"):
        icon = ""
        tag = ""
        
        if type == "HEADER":
            self.textbox_log.insert("end", "\n" + msg + "\n", "HEADER")
            self.textbox_log.see("end")
            return

        if type == "SUCCESS":
            icon = "✔ "
            tag = "GREEN"
        elif type == "WARN":
            icon = "⚠ "
            tag = "YELLOW"
        elif type == "ERROR":
            icon = "✖ "
            tag = "RED"
        elif type == "PROCESS":
            icon = "➜ "
            tag = "CYAN"
        
        self.textbox_log.insert("end", icon, tag)
        self.textbox_log.insert("end", msg + "\n")
        self.textbox_log.see("end")

    def set_registry(self, hive, path, key, value, type_reg):
        try:
            reg_key = winreg.CreateKey(hive, path)
            winreg.SetValueEx(reg_key, key, 0, type_reg, value)
            winreg.CloseKey(reg_key)
            return True, f"{key} definido para {value}"
        except Exception as e:
            return False, f"Falha em {key}: {str(e)}"

    def start_thread(self):
        self.textbox_log.delete("0.0", "end")
        self.btn_apply.configure(state="disabled", text="APLICANDO...")
        threading.Thread(target=self.run_fixes_logic, daemon=True).start()

    def run_fixes_logic(self):
        self.log("INICIANDO CONFIGURAÇÃO DE REDE", "HEADER")
        time.sleep(0.5)
        
        tasks = [
            ("blank_logon", winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Lsa", "LimitBlankPasswordUse", 0),
            ("enable_ntlmv1", winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Lsa", "LmCompatibilityLevel", 1),
            ("disable_uac", winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "EnableLUA", 0),
            ("guest_logon", winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters", "AllowInsecureGuestAuth", 1),
            ("rpc_auth_privacy", winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Print", "RpcAuthnLevelPrivacyEnabled", 0),
        ]

        # Executa tarefas padrão
        for var_name, hive, path, key, val in tasks:
            if self.vars[var_name].get():
                time.sleep(0.4) # Delay tático
                success, msg = self.set_registry(hive, path, key, val, winreg.REG_DWORD)
                if success:
                    self.log(msg, "SUCCESS")
                else:
                    self.log(msg, "ERROR")

        # Tarefas Especiais (SMB Signing requer 2 chaves)
        if self.vars["disable_smb_sign"].get():
            time.sleep(0.4)
            s1, m1 = self.set_registry(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters", "RequireSecuritySignature", 0, winreg.REG_DWORD)
            if s1: self.log("LanmanWorkstation SecuritySignature OFF", "SUCCESS")
            
            time.sleep(0.2)
            s2, m2 = self.set_registry(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "RequireSecuritySignature", 0, winreg.REG_DWORD)
            if s2: self.log("LanmanServer SecuritySignature OFF", "SUCCESS")

        if self.vars["disable_secure_negotiate"].get():
            time.sleep(0.4)
            s3, m3 = self.set_registry(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters", "RequireSecureNegotiate", 0, winreg.REG_DWORD)
            if s3: self.log("Secure Negotiate desativado", "SUCCESS")

        time.sleep(0.8)
        self.log("OPERAÇÃO CONCLUÍDA", "HEADER")
        self.log("Reinicie o computador para efetivar.", "WARN")
        
        self.btn_apply.configure(state="normal", text="APLICAR CONFIGURAÇÕES")
        try: ctypes.windll.user32.MessageBeep(0x40) 
        except: pass

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        app = LanmanTool()
        app.mainloop()

#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import time
import shutil
from pathlib import Path
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class VPSOptimizer:
    def __init__(self):
        self.log_file = f"/tmp/vps_optimizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def banner(self):
        banner_text = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║  {Colors.BOLD}{Colors.RED}██╗   ██╗██████╗ ███████╗     ██████╗ ██████╗ ████████╗██╗███╗   ███╗██╗███████╗███████╗██████╗ {Colors.RESET}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.RED}██║   ██║██╔══██╗██╔════╝    ██╔═══██╗██╔══██╗╚══██╔══╝██║████╗ ████║██║╚══███╔╝██╔════╝██╔══██╗{Colors.RESET}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.RED}██║   ██║██████╔╝███████╗    ██║   ██║██████╔╝   ██║   ██║██╔████╔██║██║  ███╔╝ █████╗  ██████╔╝{Colors.RESET}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.RED}╚██╗ ██╔╝██╔═══╝ ╚════██║    ██║   ██║██╔═══╝    ██║   ██║██║╚██╔╝██║██║ ███╔╝  ██╔══╝  ██╔══██╗{Colors.RESET}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.RED} ╚████╔╝ ██║     ███████║    ╚██████╔╝██║        ██║   ██║██║ ╚═╝ ██║██║███████╗███████╗██║  ██║{Colors.RESET}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.RED}  ╚═══╝  ╚═╝     ╚══════╝     ╚═════╝ ╚═╝        ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝{Colors.RESET}{Colors.CYAN}║
║                                                                                  ║
║  {Colors.BOLD}{Colors.YELLOW}Enterprise VPS Cleanup & Performance Optimization Suite{Colors.RESET}{Colors.CYAN}                    ║
║  {Colors.GREEN}Version 2.0 | Security & Performance Focused{Colors.RESET}{Colors.CYAN}                                ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner_text)
        
    def log_action(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        print(f"{Colors.GREEN}[LOG]{Colors.RESET} {message}")
        
    def run_command(self, cmd, check=True):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if check and result.returncode != 0:
                self.log_action(f"Command failed: {cmd}")
                self.log_action(f"Error: {result.stderr}")
                return False
            return result.stdout
        except Exception as e:
            self.log_action(f"Exception running command {cmd}: {str(e)}")
            return False
            
    def get_size(self, path):
        """Calculate total size of directory recursively"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        pass
        except PermissionError:
            pass
        return total_size

    def format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while size_bytes >= 1024 and i < len(units) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.2f} {units[i]}"

    def directory_scanner(self, target_dir="/", sort_by_size=True, limit=20):
        """Enhanced directory scanner with filtering"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}📁 Directory Scanner{Colors.RESET}")
        print(f"{Colors.CYAN}Scanning: {target_dir}{Colors.RESET}")
        print("-" * 80)
        
        if not os.path.exists(target_dir):
            print(f"{Colors.RED}Error: Directory '{target_dir}' does not exist{Colors.RESET}")
            return
        
        results = []
        
        try:
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                if os.path.isdir(item_path):
                    size = self.get_size(item_path)
                    results.append((item, size))
        except PermissionError:
            print(f"{Colors.RED}Error: Permission denied accessing '{target_dir}'{Colors.RESET}")
            return
        
        if sort_by_size:
            results.sort(key=lambda x: x[1], reverse=True)
        else:
            results.sort(key=lambda x: x[0].lower())
        
        if limit:
            results = results[:limit]
        
        max_name_len = max(len(name) for name, _ in results) if results else 20
        max_name_len = max(max_name_len, 20)
        
        print(f"{Colors.BOLD}{'Directory Name':<{max_name_len}} {'Size':>12}{Colors.RESET}")
        print("-" * (max_name_len + 15))
        
        total_size = 0
        for name, size in results:
            formatted_size = self.format_size(size)
            color = Colors.RED if size > 1024**3 else Colors.YELLOW if size > 1024**2 else Colors.GREEN
            print(f"{color}{name:<{max_name_len}} {formatted_size:>12}{Colors.RESET}")
            total_size += size
        
        print("-" * (max_name_len + 15))
        print(f"{Colors.BOLD}{'Total':<{max_name_len}} {self.format_size(total_size):>12}{Colors.RESET}")
        
    def system_cleanup(self):
        """Comprehensive system cleanup"""
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🧹 System Cleanup{Colors.RESET}")
        
        cleanup_tasks = [
            ("Cleaning package cache", "apt-get clean && apt-get autoclean"),
            ("Removing orphaned packages", "apt-get autoremove -y"),
            ("Cleaning journal logs", "journalctl --vacuum-time=7d"),
            ("Cleaning tmp files", "find /tmp -type f -atime +7 -delete"),
            ("Cleaning old log files", "find /var/log -name '*.log' -type f -mtime +30 -delete"),
            ("Cleaning thumbnail cache", "find /home -name '.thumbnails' -type d -exec rm -rf {} + 2>/dev/null || true"),
            ("Cleaning browser cache", "find /home -name '.cache' -type d -exec rm -rf {} + 2>/dev/null || true"),
            ("Cleaning crash dumps", "rm -rf /var/crash/* 2>/dev/null || true"),
            ("Cleaning old kernels", "apt-get autoremove --purge -y"),
        ]
        
        for task_name, command in cleanup_tasks:
            print(f"{Colors.CYAN}• {task_name}...{Colors.RESET}")
            if self.run_command(command, check=False):
                self.log_action(f"Completed: {task_name}")
                print(f"  {Colors.GREEN}✓ Done{Colors.RESET}")
            else:
                print(f"  {Colors.YELLOW}⚠ Skipped or failed{Colors.RESET}")
        
    def docker_cleanup(self):
        """Docker cleanup"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}🐳 Docker Cleanup{Colors.RESET}")
        
        if not self.run_command("which docker", check=False):
            print(f"{Colors.YELLOW}Docker not found, skipping...{Colors.RESET}")
            return
            
        docker_tasks = [
            ("Pruning unused containers", "docker container prune -f"),
            ("Pruning unused images", "docker image prune -a -f"),
            ("Pruning unused volumes", "docker volume prune -f"),
            ("Pruning unused networks", "docker network prune -f"),
            ("System prune", "docker system prune -a -f"),
        ]
        
        for task_name, command in docker_tasks:
            print(f"{Colors.CYAN}• {task_name}...{Colors.RESET}")
            if self.run_command(command, check=False):
                self.log_action(f"Docker: {task_name}")
                print(f"  {Colors.GREEN}✓ Done{Colors.RESET}")
        
    def optimize_system(self):
        """System optimization"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}⚡ System Optimization{Colors.RESET}")
        
        # CPU Governor
        print(f"{Colors.CYAN}• Setting CPU governor to performance...{Colors.RESET}")
        self.run_command("echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor", check=False)
        
        # Swappiness
        print(f"{Colors.CYAN}• Optimizing swappiness...{Colors.RESET}")
        self.run_command("sysctl vm.swappiness=10", check=False)
        
        # Network optimizations
        print(f"{Colors.CYAN}• Applying network optimizations...{Colors.RESET}")
        net_opts = [
            "net.core.rmem_max=134217728",
            "net.core.wmem_max=134217728",
            "net.ipv4.tcp_rmem=4096 87380 134217728",
            "net.ipv4.tcp_wmem=4096 65536 134217728",
            "net.ipv4.tcp_congestion_control=bbr",
        ]
        
        for opt in net_opts:
            self.run_command(f"sysctl {opt}", check=False)
        
        # I/O scheduler
        print(f"{Colors.CYAN}• Optimizing I/O scheduler...{Colors.RESET}")
        self.run_command("echo mq-deadline | tee /sys/block/*/queue/scheduler", check=False)
        
        self.log_action("System optimization completed")
        print(f"  {Colors.GREEN}✓ Optimization complete{Colors.RESET}")
        
    def memory_analysis(self):
        """Memory usage analysis"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}💾 Memory Analysis{Colors.RESET}")
        
        # Memory info
        mem_info = self.run_command("free -h")
        print(f"{Colors.YELLOW}Memory Usage:{Colors.RESET}")
        print(mem_info)
        
        # Top memory consumers
        print(f"\n{Colors.YELLOW}Top Memory Consumers:{Colors.RESET}")
        top_mem = self.run_command("ps aux --sort=-%mem | head -10")
        print(top_mem)
        
    def disk_analysis(self):
        """Disk usage analysis"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}💽 Disk Analysis{Colors.RESET}")
        
        # Disk usage
        disk_info = self.run_command("df -h")
        print(f"{Colors.YELLOW}Disk Usage:{Colors.RESET}")
        print(disk_info)
        
        # Largest files
        print(f"\n{Colors.YELLOW}Largest Files (>100MB):{Colors.RESET}")
        large_files = self.run_command("find / -type f -size +100M -exec ls -lh {} + 2>/dev/null | head -20", check=False)
        if large_files:
            print(large_files)
        
    def security_hardening(self):
        """Basic security hardening"""
        print(f"\n{Colors.BOLD}{Colors.RED}🔒 Security Hardening{Colors.RESET}")
        
        security_tasks = [
            ("Updating package lists", "apt-get update"),
            ("Installing security updates", "apt-get upgrade -y"),
            ("Installing fail2ban", "apt-get install -y fail2ban"),
            ("Configuring firewall", "ufw enable"),
            ("Setting secure SSH config", "sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config"),
        ]
        
        for task_name, command in security_tasks:
            print(f"{Colors.CYAN}• {task_name}...{Colors.RESET}")
            if self.run_command(command, check=False):
                self.log_action(f"Security: {task_name}")
                print(f"  {Colors.GREEN}✓ Done{Colors.RESET}")
        
    def main_menu(self):
        """Interactive main menu"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗")
            print(f"║                                  MAIN MENU                                       ║")
            print(f"╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
            
            options = [
                ("1", "🔍 Directory Scanner", "directory_scanner"),
                ("2", "🧹 System Cleanup", "system_cleanup"),
                ("3", "🐳 Docker Cleanup", "docker_cleanup"),
                ("4", "⚡ System Optimization", "optimize_system"),
                ("5", "💾 Memory Analysis", "memory_analysis"),
                ("6", "💽 Disk Analysis", "disk_analysis"),
                ("7", "🔒 Security Hardening", "security_hardening"),
                ("8", "🚀 Full Optimization Suite", "full_suite"),
                ("9", "📊 System Status", "system_status"),
                ("0", "🚪 Exit", "exit"),
            ]
            
            for num, desc, _ in options:
                print(f"{Colors.CYAN}  {num}. {desc}{Colors.RESET}")
            
            choice = input(f"\n{Colors.BOLD}{Colors.YELLOW}Select option: {Colors.RESET}")
            
            if choice == "1":
                path = input(f"{Colors.CYAN}Enter directory path (default: /): {Colors.RESET}") or "/"
                self.directory_scanner(path)
            elif choice == "2":
                self.system_cleanup()
            elif choice == "3":
                self.docker_cleanup()
            elif choice == "4":
                self.optimize_system()
            elif choice == "5":
                self.memory_analysis()
            elif choice == "6":
                self.disk_analysis()
            elif choice == "7":
                self.security_hardening()
            elif choice == "8":
                self.full_optimization_suite()
            elif choice == "9":
                self.system_status()
            elif choice == "0":
                print(f"\n{Colors.GREEN}Thanks for using VPS Optimizer!{Colors.RESET}")
                print(f"{Colors.CYAN}Log file: {self.log_file}{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Invalid option. Please try again.{Colors.RESET}")
                
    def full_optimization_suite(self):
        """Run complete optimization suite"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}🚀 Full Optimization Suite{Colors.RESET}")
        print(f"{Colors.YELLOW}This will run all optimization tasks...{Colors.RESET}")
        
        confirm = input(f"{Colors.CYAN}Continue? (y/N): {Colors.RESET}")
        if confirm.lower() != 'y':
            return
            
        self.system_cleanup()
        self.docker_cleanup()
        self.optimize_system()
        self.security_hardening()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Full optimization completed!{Colors.RESET}")
        
    def system_status(self):
        """Display system status"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 System Status{Colors.RESET}")
        
        # Uptime
        uptime = self.run_command("uptime")
        print(f"{Colors.YELLOW}Uptime:{Colors.RESET} {uptime}")
        
        # Load average
        load_avg = self.run_command("cat /proc/loadavg")
        print(f"{Colors.YELLOW}Load Average:{Colors.RESET} {load_avg}")
        
        # CPU info
        cpu_info = self.run_command("lscpu | grep 'Model name'")
        print(f"{Colors.YELLOW}CPU:{Colors.RESET} {cpu_info}")
        
        # Memory
        mem_info = self.run_command("free -h | grep Mem")
        print(f"{Colors.YELLOW}Memory:{Colors.RESET} {mem_info}")

def main():
    if os.geteuid() != 0:
        print(f"{Colors.RED}This script requires root privileges. Please run with sudo.{Colors.RESET}")
        sys.exit(1)
        
    optimizer = VPSOptimizer()
    optimizer.banner()
    
    parser = argparse.ArgumentParser(description='VPS Optimization Suite')
    parser.add_argument('--auto', action='store_true', help='Run automated optimization')
    parser.add_argument('--scan', type=str, help='Scan directory')
    
    args = parser.parse_args()
    
    if args.auto:
        optimizer.full_optimization_suite()
    elif args.scan:
        optimizer.directory_scanner(args.scan)
    else:
        optimizer.main_menu()

if __name__ == "__main__":
    main()

# VPS_D.O.C
-A VPS Optimizer Suite: With a simple yet effective interface that gets the job DONE-
A comprehensive Linux VPS cleanup and optimization tool designed for enterprise environments. Features integrated directory scanning, system cleanup, performance tuning, and security hardening.

## Features

### 🔍 Directory Scanner
- Recursive directory size calculation
- Color-coded output based on size
- Sortable by size or name
- Human-readable format (B, KB, MB, GB, TB)

### 🧹 System Cleanup
- Package cache cleaning (`apt-get clean/autoclean`)
- Orphaned package removal
- Journal log cleanup (7-day retention)
- Temporary file cleanup
- Old log file removal (30+ days)
- Browser/thumbnail cache cleanup
- Crash dump cleanup
- Old kernel removal

### 🐳 Docker Cleanup
- Unused container pruning
- Image cleanup (including dangling)
- Volume pruning
- Network cleanup
- Complete system prune

### ⚡ Performance Optimization
- CPU governor set to performance
- Swappiness optimization (vm.swappiness=10)
- Network buffer tuning
- BBR congestion control
- I/O scheduler optimization (mq-deadline)

### 🔒 Security Hardening
- Security updates installation
- Fail2ban installation/configuration
- UFW firewall activation
- SSH root login disable
- System package updates

### 📊 System Analysis
- Memory usage monitoring
- Disk space analysis
- Large file detection (>100MB)
- Top memory consumers
- System status overview

## Requirements

- Linux-based VPS (Ubuntu/Debian tested)
- Python 3.6+
- Root privileges (sudo)
- Standard Unix utilities

## Installation

1. Download the script:
```bash
wget https://raw.githubusercontent.com/your-repo/vps_optimizer.py
chmod +x vps_optimizer.py
```

2. Run with root privileges:
```bash
sudo python3 vps_optimizer.py
```

## Usage

### Interactive Mode
```bash
sudo python3 vps_optimizer.py
```
Launches the interactive menu with all available options.

### Automated Mode
```bash
sudo python3 vps_optimizer.py --auto
```
Runs complete optimization suite without user interaction.

### Directory Scan Only
```bash
sudo python3 vps_optimizer.py --scan /path/to/directory
```
Scans specified directory and displays size information.

## Menu Options

| Option | Description |
|--------|-------------|
| 1 | Directory Scanner - Analyze directory sizes |
| 2 | System Cleanup - Clean temporary files, caches, logs |
| 3 | Docker Cleanup - Remove unused Docker resources |
| 4 | System Optimization - CPU/memory/network tuning |
| 5 | Memory Analysis - Current memory usage and top consumers |
| 6 | Disk Analysis - Disk usage and large file detection |
| 7 | Security Hardening - Basic security improvements |
| 8 | Full Optimization Suite - Run all optimization tasks |
| 9 | System Status - Display current system information |
| 0 | Exit |

## Examples

### Basic System Cleanup
```bash
# Interactive cleanup
sudo python3 vps_optimizer.py
# Select option 2

# Automated full optimization
sudo python3 vps_optimizer.py --auto
```

### Directory Analysis
```bash
# Scan root directory
sudo python3 vps_optimizer.py --scan /

# Scan specific directory
sudo python3 vps_optimizer.py --scan /var/log
```

### Performance Tuning
```bash
# Run optimization only
sudo python3 vps_optimizer.py
# Select option 4
```

## Logging

All actions are logged to `/tmp/vps_optimizer_[timestamp].log` with:
- Timestamp for each action
- Command execution results
- Error messages
- Completion status

## Safety Features

- Root privilege verification
- Permission error handling
- Command execution validation
- Confirmation prompts for destructive actions
- Comprehensive error logging

## Network Optimizations Applied

```bash
net.core.rmem_max=134217728
net.core.wmem_max=134217728
net.ipv4.tcp_rmem=4096 87380 134217728
net.ipv4.tcp_wmem=4096 65536 134217728
net.ipv4.tcp_congestion_control=bbr
```

## Security Hardening Actions

- Updates all packages to latest versions
- Installs and configures fail2ban
- Enables UFW firewall
- Disables SSH root login
- Applies security patches

## Enterprise Considerations

- **Performance**: Optimized for VPS environments
- **Security**: Enterprise-grade hardening
- **Logging**: Comprehensive audit trail
- **Automation**: Scriptable for CI/CD pipelines
- **Monitoring**: Integration-ready output format

## Troubleshooting

### Permission Errors
```bash
# Ensure script runs as root
sudo python3 vps_optimizer.py
```

### Docker Not Found
The script automatically detects Docker availability and skips Docker cleanup if not installed.

### Network Optimization Issues
Some network optimizations require kernel module support. The script continues if optimizations fail.

## Supported Distributions

- Ubuntu 16.04+
- Debian 9+
- CentOS 7+ (with modifications)
- Other systemd-based distributions

## License

MIT License - Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request

## Security Note

This script requires root privileges and makes system-wide changes. Review the code before running in production environments.

## Changelog

### v2.0
- Added interactive menu system
- Integrated directory scanner
- Performance optimizations
- Security hardening features
- Comprehensive logging

### v1.0
- Initial release
- Basic cleanup functionality

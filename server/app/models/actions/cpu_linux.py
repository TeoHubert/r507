from models.host import Host

def run(host: Host) -> str:
    try:
        value = float(host.execute_ssh_command('read -r cpu user nice system idle iowait irq softirq steal guest < /proc/stat; sleep 1; read -r cpu_n user_n nice_n system_n idle_n iowait_n irq_n softirq_n steal_n guest_n < /proc/stat; PREV_TOTAL=$((user+nice+system+idle+iowait+irq+softirq+steal)); CURRENT_TOTAL=$((user_n+nice_n+system_n+idle_n+iowait_n+irq_n+softirq_n+steal_n)); PREV_IDLE=$idle; CURRENT_IDLE=$idle_n; DIFF_TOTAL=$((CURRENT_TOTAL-PREV_TOTAL)); DIFF_IDLE=$((CURRENT_IDLE-PREV_IDLE)); CPU_USAGE=$(( (DIFF_TOTAL-DIFF_IDLE) * 100 / DIFF_TOTAL )); echo "$CPU_USAGE"'))
        return value
    except Exception as e:
        return f"Error: {e}"
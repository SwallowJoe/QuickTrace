from model import Model
import re

__DEBUG = True

class CommandGenerator:
    
    def __init__(self, model):
        self.__model: Model = model
        self.__reset()

    def __reset(self):
        self.__RecordSettings = RecordSettings()
        self.__LinuxFtrace = LinuxFtrace()
        self.__LinuxSysStats = LinuxSysStats()
        self.__LinuxProcessStats = LinuxProcessStats()
        self.__AndroidPower = AndroidPower()
        self.__AndroidHeapProfd = AndroidHeapProfd()
        self.__AndroidJavaHProf = AndroidJavaHProf()
        self.__AndroidLog = AndroidLog()
        self.__AndroidFrameTimeline = AndroidFrameTimeline()
        self.__AndroidGameInterventions = AndroidGameInterventions()
        self.__AndroidNetworkPackets = AndroidNetworkPackets()
        self.__LinuxPerf = LinuxPerf()

    def generateCommand(self):
        self.__reset()
        self.__generateRecordingSettingsCommand()
        self.__generateCpuCommand()
        self.__generateGpuCommand()
        self.__generatePowerCommand()
        self.__generateMemoryCommand()
        self.__generateAndroidAppsCommand()
        self.__generateStackSamplesCommand()
        
        command = self.__RecordSettings.format()
        command += self.__LinuxFtrace.format()
        command += self.__LinuxProcessStats.format()
        command += self.__LinuxSysStats.format()
        command += self.__AndroidPower.format()
        command += self.__AndroidHeapProfd.format()
        command += self.__AndroidJavaHProf.format()
        command += self.__AndroidLog.format()
        command += self.__AndroidFrameTimeline.format()
        command += self.__AndroidGameInterventions.format()
        command += self.__AndroidNetworkPackets.format()
        command += self.__LinuxPerf.format()
        command += self.__RecordSettings.formatDuration()

        return command
    def syncCommand(self, config_content: str):
        self.__reset()

        self.__RecordSettings.unformat(config_content)
        self.__RecordSettings.unformatDuration(config_content)
        self.__LinuxFtrace.unformat(config_content)
        self.__LinuxProcessStats.unformat(config_content)
        self.__LinuxSysStats.unformat(config_content)
        self.__AndroidPower.unformat(config=config_content)
        self.__AndroidHeapProfd.unformat(config_content)
        self.__AndroidJavaHProf.unformat(config_content)
        self.__AndroidLog.unformat(config_content)
        self.__AndroidFrameTimeline.unformat(config_content)
        self.__AndroidGameInterventions.unformat(config_content)
        self.__AndroidNetworkPackets.unformat(config_content)
        self.__LinuxPerf.unformat(config_content)

        self.__model.reset()
        self.__RecordSettings.syncToModel(self.__model)
        self.__LinuxFtrace.syncToModel(self.__model)
        self.__LinuxProcessStats.syncToModel(self.__model)
        self.__LinuxSysStats.syncToModel(self.__model)
        self.__AndroidPower.syncToModel(self.__model)
        self.__AndroidHeapProfd.syncToModel(self.__model)
        self.__AndroidJavaHProf.syncToModel(self.__model)
        self.__AndroidLog.syncToModel(self.__model)
        self.__AndroidFrameTimeline.syncToModel(self.__model)
        self.__AndroidGameInterventions.syncToModel(self.__model)
        self.__AndroidNetworkPackets.syncToModel(self.__model)
        self.__LinuxPerf.syncToModel(self.__model)

    ########## record settings ##########
    def __getCurrentFillPolicy(self):
        fill_policy = 'DISCARD'
        fill_mode = self.__model.recordingMode.get()
        if fill_mode == 1: # Stop When Full
            fill_policy = 'DISCARD'
        elif fill_mode == 2: # Ring buffer
            fill_policy = 'RING_BUFFER'
        else:
            fill_policy = 'DISCARD'
        return fill_policy
    def __getCurrentBufferSizeOfFirstBuffers(self):
        buffer_size = self.__model.memoryBufferSize.get() * 1024 - self.__getCurrentBufferSizeOfSecondBuffers()
        return buffer_size
    def __getCurrentBufferSizeOfSecondBuffers(self):
        buffer_size = 512
        if self.__model.memoryBufferSize.get() < 8:
            buffer_size = 512
        elif self.__model.memoryBufferSize.get() < 16:
            buffer_size = 1024
        else:        
            buffer_size = 2048
        return buffer_size
    def __generateRecordingSettingsCommand(self):
        fill_mode = self.__model.recordingMode.get()
        first_buffer_size = self.__getCurrentBufferSizeOfFirstBuffers()
        second_buffer_size = self.__getCurrentBufferSizeOfSecondBuffers()
        duration = self.__model.recordingDuration.get()
        self.__RecordSettings.setFillMode(fill_mode)
        self.__RecordSettings.setFirstBufferSize(first_buffer_size)
        self.__RecordSettings.setSecondBufferSize(second_buffer_size)
        self.__RecordSettings.setRecordDuration(duration)

    ############################## CPU ###########################
    def __generateCpuCommand(self):
        enableCpuUsageCounter = self.__model.enableCpuUsageCounter.get() == 1
        enableCpuFreq = self.__model.enableCpuFreq.get() == 1
        enableCpuSyscalls = self.__model.enableSyscalls.get() == 1
        enableCpuSchedulingDetials = self.__model.enableCpuSchedulingDetails.get() == 1

        if enableCpuUsageCounter:
            # stat_period_ms
            self.__LinuxSysStats.setCpuStatPeriod(self.__getCurrentCpuUsageCounterInterval())
            self.__LinuxSysStats.addEvents('stat_counters', 'STAT_CPU_TIMES')
            self.__LinuxSysStats.addEvents('stat_counters', 'STAT_FORK_COUNT')
        if enableCpuSchedulingDetials:
            self.__LinuxProcessStats.addEvents('scan_all_processes_on_start', 'true')
            self.__LinuxFtrace.addEvents('sched/sched_switch')
            self.__LinuxFtrace.addEvents('power/suspend_resume')
            self.__LinuxFtrace.addEvents('sched/sched_wakeup')
            self.__LinuxFtrace.addEvents('sched/sched_wakeup_new')
            self.__LinuxFtrace.addEvents('sched/sched_waking')
            self.__LinuxFtrace.addEvents('sched/sched_process_exit')
            self.__LinuxFtrace.addEvents('sched/sched_process_free')
            self.__LinuxFtrace.addEvents('task/task_newtask')
            self.__LinuxFtrace.addEvents('task/task_rename')

        if enableCpuFreq:
            self.__LinuxSysStats.setCpuFreqPeriod(self.__getCurrentCpuFreq())
            self.__LinuxFtrace.addEvents('power/cpu_frequency')
            self.__LinuxFtrace.addEvents('power/cpu_idle')
            self.__LinuxFtrace.addEvents('power/suspend_resume')
        if enableCpuSyscalls:
            self.__LinuxFtrace.addEvents('raw_syscalls/sys_enter')
            self.__LinuxFtrace.addEvents('raw_syscalls/sys_exit')

    def __getCurrentCpuUsageCounterInterval(self):
        return self.__model.cpuUsageCounterInterval.get()

    def __getCurrentCpuFreq(self):
        return self.__model.cpuFreqInterval.get()

    ############################## GPU ###########################
    def __generateGpuCommand(self):
        enableGpuFreq = self.__model.enableGpuFreq.get() == 1
        enableGpuMemory = self.__model.enableGpuMemory.get() == 1
        enableGpuWorkPeriod = self.__model.enableGpuWorkPeriod == 1

        if enableGpuFreq:
            self.__LinuxFtrace.addEvents('power/gpu_frequency')
        if enableGpuMemory:
            self.__LinuxFtrace.addEvents('gpu_mem/gpu_mem_total')
        if enableGpuWorkPeriod:
            self.__LinuxFtrace.addEvents('gpu_mem/gpu_mem_total')

    ############################## Power ###########################
    def __generatePowerCommand(self):
        enableBatteryDrain = self.__model.enableBatteryDrain.get() == 1
        enableVoltages = self.__model.enableVoltages.get() == 1
        
        if enableBatteryDrain:
            self.__AndroidPower.setPollInterval(self.__getCurrentBatteryPollMs())
        if enableVoltages:
            self.__LinuxFtrace.addEvents('regulator/regulator_set_voltage')
            self.__LinuxFtrace.addEvents('regulator/regulator_set_voltage_complete')
            self.__LinuxFtrace.addEvents('power/clock_enable')
            self.__LinuxFtrace.addEvents('power/clock_disable')
            self.__LinuxFtrace.addEvents('power/clock_set_rate')
            self.__LinuxFtrace.addEvents('power/suspend_resume')

    def __getCurrentBatteryPollMs(self):
        return self.__model.batteryDrainInterval.get()
    
    ############################## Memory ###########################
    def __generateMemoryCommand(self):
        # print('__generateMemoryCommand')
        self.__handleNativeHeapProfiling()
        self.__handleJavaHeapDumps()
        self.__handleKernelMeminfo()
        self.__handleHighMemEvents()
        self.__handleLMK()
        self.__handleNativePerProcessStats()
    def __handleNativeHeapProfiling(self):
        enableNativeHeap = self.__model.enableNativeHeap.get() == 1
        if not enableNativeHeap:
            return
        self.__AndroidHeapProfd.enable()
        self.__AndroidHeapProfd.setProcessCmdlines(self.__model.nativeHeapProcessCmdlines.get())
        self.__AndroidHeapProfd.setSamplingIntervalBytes(self.__model.nativeHeapSamplingInterval.get())
        self.__AndroidHeapProfd.setDumpInterval(self.__model.nativeHeapDumpsInterval.get())
        self.__AndroidHeapProfd.setDumpPhase(self.__model.nativeHeapDumpPhase.get())
        self.__AndroidHeapProfd.setShmemSizeBytes(self.__model.nativeHeapSharedMemory.get())
        if self.__model.enableBlockClient.get() == 1:
            self.__AndroidHeapProfd.enableBlockClient()
        if self.__model.enableAllCustomAllocators.get() == 1:
            self.__AndroidHeapProfd.enableAllCustomAllocator()
    
    def __handleJavaHeapDumps(self):
        enableJavaHeapDumps = self.__model.enableJavaHeap.get() == 1
        if not enableJavaHeapDumps:
            return
        self.__AndroidJavaHProf.enable()
        self.__AndroidJavaHProf.setProcessCmdlines(self.__model.javaHeapProcessCmdlines.get())
        self.__AndroidJavaHProf.setDumpInterval(self.__model.javaHeapDumpsInterval.get())
        self.__AndroidJavaHProf.setDumpPhase(self.__model.javaHeapDumpsPhase.get())

    def __handleKernelMeminfo(self):
        if self.__model.enableKernelMeminfo.get() == 1:
            interval = self.__model.kernelMeminfoInterval.get()
            self.__LinuxSysStats.setMeminfoPeriod(interval)
            for counter in self.__model.kernelMeminfoCounters:
                self.__LinuxSysStats.addEvents('meminfo_counters', f'MEMINFO_{counter.upper()}')
    def __handleHighMemEvents(self):
        if self.__model.enableHighFreqMemEvents.get() == 1: 
            self.__LinuxProcessStats.addEvents('scan_all_processes_on_start', 'true')
            self.__LinuxFtrace.addEvents('mm_event/mm_event_record')
            self.__LinuxFtrace.addEvents('kmem/rss_stat')
            self.__LinuxFtrace.addEvents('ion/ion_stat')
            self.__LinuxFtrace.addEvents('dmabuf_heap/dma_heap_stat')
            self.__LinuxFtrace.addEvents('kmem/ion_heap_grow')
            self.__LinuxFtrace.addEvents('kmem/ion_heap_shrink')
            self.__LinuxFtrace.addEvents('sched/sched_process_exit')
            self.__LinuxFtrace.addEvents('sched/sched_process_free')
            self.__LinuxFtrace.addEvents('task/task_newtask')
            self.__LinuxFtrace.addEvents('task/task_rename')

    def __handleLMK(self):
        if self.__model.enableLMK.get() == 1:
            self.__LinuxProcessStats.addEvents('scan_all_processes_on_start', 'true')
            self.__LinuxFtrace.addEvents('lowmemorykiller/lowmemory_kill')
            self.__LinuxFtrace.addEvents('oom/oom_score_adj_update')
            self.__LinuxFtrace.addEvents('ftrace/print')
            self.__LinuxFtrace.addEvents('lmkd')

    def __handleNativePerProcessStats(self):
        if self.__model.enablePerPorcessStats.get() == 1:
            interval = self.__model.perProcessStatsInterval.get()
            self.__LinuxProcessStats.addEvents('proc_stats_poll_ms', interval)

    ############################## Android Apps ###########################
    def __generateAndroidAppsCommand(self):
        # print('__generateAndroidAppsCommand')
        self.__handleAtraceCategories()
        self.__handleEventLogs()
        self.__handleFrameTimeline()
        self.__handleGameIntervention()
        self.__handleNetworkTracing()
    
    def __handleAtraceCategories(self):
        if self.__model.enableAtraceUserspaceAnnotations.get() == 1:
            for category in self.__model.atraceCategories:
                self.__LinuxFtrace.addAtraceCategory(category)
            if self.__model.enableRecordAllApps.get() == 1:
                self.__LinuxFtrace.addAtraceProcess('*')
            else:
                processes = split_and_filter_empty_lines(self.__model.atraceProcesses.get())
                for app in processes:
                    self.__LinuxFtrace.addAtraceProcess(app)

    def __handleEventLogs(self):
        if self.__model.enableEventLog.get() == 1:
            for eventId in self.__model.eventLogBuffers:
                self.__AndroidLog.addLogId(eventId)
    def __handleFrameTimeline(self):
        if self.__model.enableFrameTimeline.get() == 1:
            self.__AndroidFrameTimeline.enableFrametimeLine()
    def __handleGameIntervention(self):
        if self.__model.enableGameInterventionList.get() == 1:
            self.__AndroidGameInterventions.enableGameInterventions()
    def __handleNetworkTracing(self):
        if self.__model.enableNetworkTracing.get() == 1:
            self.__AndroidNetworkPackets.enableNetworkPacketTrace()
            self.__AndroidNetworkPackets.updateNetworkPacketPollInterval(self.__model.networkTracingInterval.get())
    ############################## StackSamples ###########################
    def __generateStackSamplesCommand(self):
        # print('__generateStackSamplesCommand')
        if self.__model.enableCallstackSampling.get() == 1:
            self.__LinuxPerf.setFrequency(self.__model.callstackSamplingFreq.get())
            self.__LinuxPerf.setProcessesCmdline(self.__model.callstackSamplingPrcesses.get())

    def __linesOf(self, string_with_lines):
        return string_with_lines.count('\n') + 1

def log(message: str):
    if __DEBUG:
        print(message)

class RecordSettings:
    def __init__(self):
        self.__fill_mode = 0
        self.__first_buffer_size = 0
        self.__second_buffer_size = 0
        self.__duration ='00:00:10'
        pass
    def syncToModel(self, model: Model):
        model.recordingDuration.set(self.__duration)
        model.recordingMode.set(self.__fill_mode)
        model.memoryBufferSize.set((self.__first_buffer_size + self.__second_buffer_size)/1024)
    def setFillMode(self, fill_mode: int):
        self.__fill_mode = fill_mode
    def setFirstBufferSize(self, bufferSize: int):
        self.__first_buffer_size = bufferSize
    def setSecondBufferSize(self, bufferSize: int):
        self.__second_buffer_size = bufferSize
    def setRecordDuration(self, duration: str):
        self.__duration = duration
    def formatDuration(self):
        # 分解 duration 字符串
        hours, minutes, seconds = map(int, self.__duration.split(':'))
        # 将小时、分钟和秒转换为毫秒
        durationInMs = (hours * 3600 + minutes * 60 + seconds) * 1000
        return f"\nduration_ms: {durationInMs}\n"
    def unformatDuration(self, config: str):
        # 使用正则表达式提取配置信息
        duration_match = re.search(r'duration_ms:\s*(\d+)', config)
        if duration_match:
            # 更新 duration
            hours, remainder = divmod(int(duration_match.group(1)) // 1000, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.setRecordDuration(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    def __getFillPolicy(self):
        if self.__fill_mode == 1: # Stop When Full
            return 'DISCARD'
        elif self.__fill_mode == 2: # Ring buffer
            return 'RING_BUFFER'
        else:
            return 'DISCARD'
    def __getFillMode(self, fill_policy: str):
        if 'DISCARD' == fill_policy:
            return 1
        elif 'RING_BUFFER' == fill_policy:
            return 2
        return 0
    def format(self):
        config  = f'buffers: {{\n'
        config += f'    size_kb: {self.__first_buffer_size}\n'
        config += f'    fill_policy: {self.__getFillPolicy()}\n'
        config += f'}}\n'
        config += f'buffers: {{\n'
        config += f'    size_kb: {self.__second_buffer_size}\n'
        config += f'    fill_policy: {self.__getFillPolicy()}\n'
        config += f'}}\n'
        config += f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.packages_list\"\n'
        config += f'        target_buffer: 1\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config

    def unformat(self, config: str):
        # 正则表达式匹配所有 buffers 块
        buffer_blocks = re.findall(r'buffers:\s*\{([\s\S]*?)\}', config)

        buffer_index = 0
        for block in buffer_blocks:
            # 在每个 buffer 块中匹配 size_kb 和 fill_policy
            size_kb_match = re.search(r'size_kb:\s*(\d+)', block)
            fill_policy_match = re.search(r'fill_policy:\s*(\w+)', block)
            
            if size_kb_match and fill_policy_match:
                size_kb = int(size_kb_match.group(1))
                fill_policy = fill_policy_match.group(1)
                
                # 根据 buffer_index 设置相应的 buffer 大小和 fill_policy
                if buffer_index == 0:
                    self.setFirstBufferSize(size_kb)
                elif buffer_index == 1:
                    self.setSecondBufferSize(size_kb)
                else:
                    # 如果有更多 buffer，可以在这里添加逻辑处理它们
                    pass
                
                # 记录所有 fill_policy
                self.setFillMode(self.__getFillMode(fill_policy))
                
                buffer_index += 1
class LinuxFtrace:
    def __init__(self):
        self.__ftrace_configs = []
        self.__atrace_categories = []
        self.__atrace_apps = []
    def addEvents(self, events: str):
        if events not in self.__ftrace_configs:
            self.__ftrace_configs.append(events)
    def removeEvent(self, events: str):
        self.__ftrace_configs.remove(events)
    def addAtraceCategory(self, category):
        self.addEvents('ftrace/print')
        if category not in self.__atrace_categories:
            self.__atrace_categories.append(category)
    def addAtraceProcess(self, process: str):
        __process = process.strip()
        if __process not in self.__atrace_apps:
            self.__atrace_apps.append(__process)
    def syncToModel(self, model: Model):
        # print('syncToModel')
        if 'raw_syscalls/sys_enter' in self.__ftrace_configs:
            model.enableSyscalls.set(1)
        if 'sched/sched_wakeup_new' in self.__ftrace_configs:
            model.enableCpuSchedulingDetails.set(1)
        if 'power/gpu_frequency' in self.__ftrace_configs:
            model.enableGpuFreq.set(1)
        if 'gpu_mem/gpu_mem_total' in self.__ftrace_configs:
            model.enableGpuMemory.set(1)
        if 'power/gpu_work_period' in self.__ftrace_configs:
            model.enableGpuWorkPeriod.set(1)
        if 'regulator/regulator_set_voltage' in self.__ftrace_configs:
            model.enableVoltages.set(1)
        if 'kmem/ion_heap_shrink' in self.__ftrace_configs:
            model.enableHighFreqMemEvents.set(1)
        if 'lowmemorykiller/lowmemory_kill' in self.__ftrace_configs:
            model.enableLMK.set(1)
        
        if len(self.__atrace_categories) > 0:
            model.enableAtraceUserspaceAnnotations.set(1)
            model.atraceCategories.clear()
            model.atraceCategories += self.__atrace_categories
            if len(self.__atrace_apps) > 0:
                # print(f'__atrace_apps={self.__atrace_apps}')
                if '*' in self.__atrace_apps:
                    model.enableRecordAllApps.set(0)
                else:
                    model.enableRecordAllApps.set(1)
                    processes = ''
                    for process in self.__atrace_apps:
                        processes += f'{process}\n'
                    model.atraceProcesses.set(processes[0:-1])

    def format(self):
        if len(self.__ftrace_configs) == 0:
            return ''
        config = ''
        if 'gpu_mem/gpu_mem_total' in self.__ftrace_configs:
            config += f"data_sources: {{\n"
            config += f"    config {{\n"
            config += f"        name: \"android.gpu.memory\"\n"
            config += f"    }}\n"
            config += f"}}\n"
        config += f"data_sources: {{\n"
        config += f"    config {{\n"
        config += f"        name: \"linux.ftrace\"\n"
        config += f"        ftrace_config {{\n"
        for event in self.__ftrace_configs:
            config += f"            ftrace_events: \"{event}\"\n"
        for category in self.__atrace_categories:
            config += f"            atrace_categories: \"{category}\"\n"
        for app in self.__atrace_apps:
            config += f"            atrace_apps: \"{app}\"\n"
        config += f"        }}\n"
        config += f"    }}\n"
        config += f"}}\n"

        return config

    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        ftrace_config_start = re.search(r'ftrace_config\s*\{', config)
        if ftrace_config_start:
            start_pos = ftrace_config_start.end()
            level = 1
            end_pos = start_pos

            # 找到 ftrace_config 的结束位置
            while level > 0 and end_pos < len(config):
                char = config[end_pos]
                if char == '{':
                    level += 1
                elif char == '}':
                    level -= 1
                end_pos += 1

            if level == 0:
                ftrace_config_content = config[start_pos:end_pos - 1]

                # 清空现有的配置
                self.__ftrace_configs.clear()
                self.__atrace_categories.clear()
                self.__atrace_apps.clear()

                # 提取配置信息
                ftrace_events_matches = re.findall(r'ftrace_events:\s*"(.*)"', ftrace_config_content)
                atrace_categories_matches = re.findall(r'atrace_categories:\s*"(.*)"', ftrace_config_content)
                atrace_apps_matches = re.findall(r'atrace_apps:\s*"(.*)"', ftrace_config_content)

                # print(f'unformat ftrace_events_matches={ftrace_events_matches}')
                for event in ftrace_events_matches:
                    self.__ftrace_configs.append(event)

                for category in atrace_categories_matches:
                    self.__atrace_categories.append(category)

                for app in atrace_apps_matches:
                    self.__atrace_apps.append(app)
class LinuxSysStats:
    def __init__(self):
        self.__meminfo_period_ms = 0
        self.__stat_period_ms = 0
        self.__cpufreq_period_ms = 0
        self.__sys_stats_configs = {}
    def clear(self):
        self.__sys_stats_configs.clear()
    def setCpuStatPeriod(self, interval: int):
        self.__stat_period_ms = interval
    def setCpuFreqPeriod(self, interval: int):
        self.__cpufreq_period_ms = interval
    def setMeminfoPeriod(self, interval: int):
        self.__meminfo_period_ms = interval
    def addEvents(self, first: str, second: str):
        # print(f'addEvent={first},{second}')
        self.__sys_stats_configs[second] = first
    def removeEvent(self, value: str):
        del self.__sys_stats_configs[value]
    def syncToModel(self, model: Model):
        if self.__stat_period_ms > 0 :
            model.enableCpuUsageCounter.set(1)
            model.cpuUsageCounterInterval.set(self.__stat_period_ms)
        if self.__cpufreq_period_ms > 0 :
            model.enableCpuFreq.set(1)
            # print(f'cpuFreq={self.__cpufreq_period_ms}')
            model.cpuFreqInterval.set(self.__cpufreq_period_ms)
        if 'meminfo_counters' in self.__sys_stats_configs.values():
            model.enableKernelMeminfo.set(1)
            model.kernelMeminfoInterval.set(self.__meminfo_period_ms)
            model.kernelMeminfoCounters.clear()
            for second, first in self.__sys_stats_configs.items():
                if first == 'meminfo_counters':
                    model.kernelMeminfoCounters.append(second)
    def format(self):
        if len(self.__sys_stats_configs) == 0:
            return ''
        config = f"data_sources: {{\n"
        config += f"    config {{\n"
        config += f"        name: \"linux.sys_stats\"\n"
        config += f"        sys_stats_config  {{\n"
        if self.__meminfo_period_ms > 0:
            config += f"            meminfo_period_ms: {self.__meminfo_period_ms}\n"
        for second,first in self.__sys_stats_configs.items():
            config += f"            {first}: {second}\n"
        if self.__stat_period_ms > 0:
            config += f"            stat_period_ms: {self.__stat_period_ms}\n"
        if self.__cpufreq_period_ms > 0:
            config += f"            cpufreq_period_ms: {self.__cpufreq_period_ms}\n"
        config += f"        }}\n"
        config += f"    }}\n"
        config += f"}}\n"
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        sys_stats_config_start = re.search(r'sys_stats_config\s*\{', config)
        if sys_stats_config_start:
            start_pos = sys_stats_config_start.end()
            level = 1
            end_pos = start_pos

            # 找到 sys_stats_config 的结束位置
            while level > 0 and end_pos < len(config):
                char = config[end_pos]
                if char == '{':
                    level += 1
                elif char == '}':
                    level -= 1
                end_pos += 1

            if level == 0:
                sys_stats_config_content = config[start_pos:end_pos - 1]

                # 清空现有的配置
                self.clear()

                # 提取配置信息
                meminfo_period_match = re.search(r'meminfo_period_ms:\s*(\d+)', sys_stats_config_content)
                stat_period_match = re.search(r'stat_period_ms:\s*(\d+)', sys_stats_config_content)
                cpufreq_period_match = re.search(r'cpufreq_period_ms:\s*(\d+)', sys_stats_config_content)
                event_matches = re.findall(r'(\w+):\s*(\w+)', sys_stats_config_content)

                if meminfo_period_match:
                    self.setMeminfoPeriod(int(meminfo_period_match.group(1)))

                if stat_period_match:
                    self.setCpuStatPeriod(int(stat_period_match.group(1)))

                if cpufreq_period_match:
                    self.setCpuFreqPeriod(int(cpufreq_period_match.group(1)))

                for event, value in event_matches:
                    self.addEvents(event, value)
class LinuxProcessStats:
    def __init__(self):
        self.__process_stats_configs = {}
        pass
    def addEvents(self, first: str, second: str):
        # print(f'addEvent={first},{second}')
        self.__process_stats_configs[first] = second
    def removeEvent(self, value: str):
        del self.__process_stats_configs[value]
    def syncToModel(self, model: Model):
        # print(f'syncToModel')
        if 'proc_stats_poll_ms' in self.__process_stats_configs.keys():
            model.enablePerPorcessStats.set(1)
            model.perProcessStatsInterval.set(int(self.__process_stats_configs['proc_stats_poll_ms']))
    def format(self):
        if len(self.__process_stats_configs) == 0:
            return ''
        config  = f"data_sources: {{\n"
        config += f"    config {{\n"
        config += f"        name: \"linux.process_stats\"\n"
        config += f"        target_buffer: 1\n"
        config += f"        process_stats_config  {{\n"
        for first,second in self.__process_stats_configs.items():
            config += f"            {first}: {second}\n"
        config += f"        }}\n"
        config += f"    }}\n"
        config += f"}}\n"
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        process_stats_config_start = re.search(r'process_stats_config\s*\{', config)
        if process_stats_config_start:
            start_pos = process_stats_config_start.end()
            level = 1
            end_pos = start_pos

            # 找到 process_stats_config 的结束位置
            while level > 0 and end_pos < len(config):
                char = config[end_pos]
                if char == '{':
                    level += 1
                elif char == '}':
                    level -= 1
                end_pos += 1

            if level == 0:
                process_stats_config_content = config[start_pos:end_pos - 1]

                # 清空现有的配置
                self.__process_stats_configs.clear()

                # 提取配置信息
                event_matches = re.findall(r'(\w+):\s*(\w+)', process_stats_config_content)
                for event, value in event_matches:
                    self.addEvents(event, value)

class AndroidPower:
    def __init__(self):
        self.__battery_poll_ms = 0
        pass
    def setPollInterval(self, battery_poll_ms: int):
        self.__battery_poll_ms = battery_poll_ms
    def syncToModel(self, model: Model):
        if self.__battery_poll_ms > 0:
            model.enableBatteryDrain.set(1)
            model.batteryDrainInterval.set(self.__battery_poll_ms)
    def format(self):
        if self.__battery_poll_ms <= 0:
            return ''
        return f"""
data_sources: {{
    config {{
        name: "android.power"
        android_power_config {{
            battery_poll_ms: {self.__battery_poll_ms}
            battery_counters: BATTERY_COUNTER_CAPACITY_PERCENT
            battery_counters: BATTERY_COUNTER_CHARGE
            battery_counters: BATTERY_COUNTER_CURRENT
            collect_power_rails: true
        }}
    }}
}}
"""
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        android_power_config_start = re.search(r'android_power_config\s*\{', config)
        if android_power_config_start:
            start_pos = android_power_config_start.end()
            level = 1
            end_pos = start_pos

            # 找到 android_power_config 的结束位置
            while level > 0 and end_pos < len(config):
                char = config[end_pos]
                if char == '{':
                    level += 1
                elif char == '}':
                    level -= 1
                end_pos += 1

            if level == 0:
                android_power_config_content = config[start_pos:end_pos - 1]

                # 提取 battery_poll_ms
                battery_poll_match = re.search(r'battery_poll_ms:\s*(\d+)', android_power_config_content)
                if battery_poll_match:
                    self.setPollInterval(int(battery_poll_match.group(1)))

class AndroidHeapProfd:
    def __init__(self):
        self.__enable = False
        self.__sampling_interval_bytes: int = 0
        self.__process_cmdlines = []
        self.__process_pids = []
        self.__dump_phase_ms = 0
        self.__dump_interval_ms = 0
        self.__shmem_size_bytes = 0
        self.__block_client = 'false'
        self.__all_heaps = 'false'
        pass
    def enable(self):
        self.__enable = True
    def setSamplingIntervalBytes(self, bytes: int):
        self.__sampling_interval_bytes = bytes
    def setProcessCmdlines(self, processCmdlines:str):
        cmdlines = split_and_filter_empty_lines(processCmdlines)
        for cmdline in cmdlines:
            if cmdline.isdigit():
                pid = int(cmdline)
                if pid < 0:
                    continue
                if pid not in self.__process_pids:
                    self.__process_pids.append(pid)
            else:
                if cmdline not in self.__process_cmdlines:
                    self.__process_cmdlines.append(cmdline)
    def setDumpPhase(self, phase: int):
        self.__dump_phase_ms = phase
    def setDumpInterval(self, interval: int):
        self.__dump_interval_ms = interval
    def setShmemSizeBytes(self, bytes: int):
        self.__shmem_size_bytes = bytes
    def enableBlockClient(self):
        self.__block_client = 'true'
    def enableAllCustomAllocator(self):
        self.__all_heaps = 'true'
    def syncToModel(self, model: Model):
        if self.__enable:
            model.enableNativeHeap.set(1)
        model.nativeHeapDumpsInterval.set(self.__dump_interval_ms)
        model.nativeHeapDumpPhase.set(self.__dump_phase_ms)
        processCmdlines = ''
        for process_cmdline in self.__process_cmdlines:
            processCmdlines += f'{process_cmdline}\n'
        for pid in self.__process_pids:
            processCmdlines += f'{pid}\n'
        # print(f'syncToModel nativeHeapProcessCmdlines=\n{processCmdlines[:-1]}')
        model.nativeHeapProcessCmdlines.set(processCmdlines[:-1])
        if self.__block_client != 'false':
            model.enableBlockClient.set(1)
        if self.__all_heaps != 'false':
            model.enableAllCustomAllocators.set(1)
        model.nativeHeapSharedMemory.set(self.__shmem_size_bytes)
        model.nativeHeapSamplingInterval.set(self.__sampling_interval_bytes)
    def format(self):
        if not self.__enable:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.heapprofd\"\n'
        config += f'        target_buffer: 0\n'
        config += f'        heapprofd_config {{\n'
        config += f'            sampling_interval_bytes: {self.__sampling_interval_bytes}\n'
        for process_cmdline in self.__process_cmdlines:
            config += f'            process_cmdline: \"{process_cmdline}\"\n'
        for pid in self.__process_pids:
            config += f'            pid: {pid}\n'
        if self.__dump_interval_ms > 0:
            config += f'            continuous_dump_config {{\n'
            config += f'                dump_interval_ms: {self.__dump_interval_ms}\n'
            if self.__dump_phase_ms > 0:
                config += f'                dump_phase_ms: {self.__dump_phase_ms}\n'
            config += f'            }}\n'
        if self.__shmem_size_bytes > 0:
            config += f'            shmem_size_bytes: {self.__shmem_size_bytes}\n'
        if self.__block_client:
            config += f'            block_client: true\n'
        else:
            config += f'            block_client: false\n'
        if self.__all_heaps:
            config += f'            all_heaps: true\n'
        config += f'        }}\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        heapprofd_config_start = re.search(r'heapprofd_config\s*\{', config)
        if heapprofd_config_start:
            start_pos = heapprofd_config_start.end()
            level = 1
            end_pos = start_pos

            # 找到 heapprofd_config 的结束位置
            while level > 0 and end_pos < len(config):
                char = config[end_pos]
                if char == '{':
                    level += 1
                elif char == '}':
                    level -= 1
                end_pos += 1

            if level == 0:
                heapprofd_config_content = config[start_pos:end_pos - 1]

                # 提取 sampling_interval_bytes
                sampling_interval_match = re.search(r'sampling_interval_bytes:\s*(\d+)', heapprofd_config_content)
                if sampling_interval_match:
                    self.setSamplingIntervalBytes(int(sampling_interval_match.group(1)))

                # 提取 process_cmdline
                process_cmdlines_matches = re.findall(r'process_cmdline:\s*"(.*)"', heapprofd_config_content)
                for cmdline in process_cmdlines_matches:
                    # print(f'nativeHeap unforamt: {cmdline}')
                    self.__process_cmdlines.append(cmdline)

                # 提取 pid
                process_pids_matches = re.findall(r'pid:\s*(\d+)', heapprofd_config_content)
                for pid in process_pids_matches:
                    self.__process_pids.append(str(pid))

                # 提取 continuous_dump_config
                dump_interval_match = re.search(r'dump_interval_ms:\s*(\d+)', heapprofd_config_content)
                dump_phase_match = re.search(r'dump_phase_ms:\s*(\d+)', heapprofd_config_content)

                if dump_interval_match:
                    self.setDumpInterval(int(dump_interval_match.group(1)))

                if dump_phase_match:
                    self.setDumpPhase(int(dump_phase_match.group(1)))

                # 提取 shmem_size_bytes
                shmem_size_match = re.search(r'shmem_size_bytes:\s*(\d+)', heapprofd_config_content)
                if shmem_size_match:
                    self.setShmemSizeBytes(int(shmem_size_match.group(1)))

                # 提取 block_client
                block_client_match = re.search(r'block_client:\s*(true|false)', heapprofd_config_content)
                if block_client_match:
                    self.__block_client = block_client_match.group(1)

                # 提取 all_heaps
                all_heaps_match = re.search(r'all_heaps:\s*(true|false)', heapprofd_config_content)
                if all_heaps_match:
                    self.__all_heaps = all_heaps_match.group(1)
                self.__enable = True
class AndroidJavaHProf:
    def __init__(self):
        self.__enable = False
        self.__process_cmdlines = []
        self.__process_pids = []
        self.__dump_phase_ms = 0
        self.__dump_interval_ms = 0
        pass
    def enable(self):
        self.__enable = True
    def setDumpPhase(self, phase: int):
        self.__dump_phase_ms = phase
    def setDumpInterval(self, interval: int):
        self.__dump_interval_ms = interval
    def setProcessCmdlines(self, processCmdlines:str):
        cmdlines = split_and_filter_empty_lines(processCmdlines)
        for cmdline in cmdlines:
            if cmdline.isdigit():
                pid = int(cmdline)
                if pid < 0:
                    continue
                if pid not in self.__process_pids:
                    self.__process_pids.append(pid)
            else:
                if cmdline not in self.__process_cmdlines:
                    self.__process_cmdlines.append(cmdline)
    def syncToModel(self, model: Model):
        if self.__enable:
            model.enableJavaHeap.set(1)
        # print(f'javaHeapDumpInterval={self.__dump_interval_ms}')
        model.javaHeapDumpsInterval.set(self.__dump_interval_ms)
        model.javaHeapDumpsPhase.set(self.__dump_phase_ms)
        processCmdlines = ''
        for process_cmdline in self.__process_cmdlines:
            processCmdlines += f'{process_cmdline}\n'
        for pid in self.__process_pids:
            processCmdlines += f'{pid}\n'
        # print(f'syncToModel javaHeapProcessCmdlines=\n{processCmdlines[:-1]}')
        model.javaHeapProcessCmdlines.set(processCmdlines[:-1])
    def format(self):
        if not self.__enable:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.java_hprof\"\n'
        config += f'        target_buffer: 0\n'
        config += f'        java_hprof_config {{\n'
        for process_cmdline in self.__process_cmdlines:
            config += f'            process_cmdline: \"{process_cmdline}\"\n'
        for pid in self.__process_pids:
            config += f'            pid: {pid}\n'
        if self.__dump_interval_ms > 0:
            config += f'            continuous_dump_config {{\n'
            config += f'                dump_interval_ms: {self.__dump_interval_ms}\n'
            if self.__dump_phase_ms > 0:
                config += f'                dump_phase_ms: {self.__dump_phase_ms}\n'
            config += f'            }}\n'
        config += f'        }}\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        java_hprof_config_start = re.search(r'java_hprof_config\s*\{', config)
        if java_hprof_config_start:
            start_pos = java_hprof_config_start.end()
            level = 1
            end_pos = start_pos

            # 找到 java_hprof_config 的结束位置
            while level > 0 and end_pos < len(config):
                char = config[end_pos]
                if char == '{':
                    level += 1
                elif char == '}':
                    level -= 1
                end_pos += 1

            if level == 0:
                java_hprof_config_content = config[start_pos:end_pos - 1]

                # 提取 process_cmdline
                process_cmdlines_matches = re.findall(r'process_cmdline:\s*"(.*)"', java_hprof_config_content)
                for cmdline in process_cmdlines_matches:
                    self.__process_cmdlines.append(cmdline)

                # 提取 pid
                process_pids_matches = re.findall(r'pid:\s*(\d+)', java_hprof_config_content)
                for pid in process_pids_matches:
                    self.__process_pids.append(str(pid))

                # 提取 continuous_dump_config
                dump_interval_match = re.search(r'dump_interval_ms:\s*(\d+)', java_hprof_config_content)
                dump_phase_match = re.search(r'dump_phase_ms:\s*(\d+)', java_hprof_config_content)

                if dump_interval_match:
                    self.setDumpInterval(int(dump_interval_match.group(1)))

                if dump_phase_match:
                    self.setDumpPhase(int(dump_phase_match.group(1)))
                self.__enable = True
            
class AndroidLog:
    def __init__(self):
        self.__log_ids = []
        pass
    def addLogId(self, logId: str):
        if logId not in self.__log_ids:
            self.__log_ids.append(logId)
    def syncToModel(self, model: Model):
        # print('AndroidLog syncToModel')
        if len(self.__log_ids) > 0:
            model.enableEventLog.set(1)
            model.eventLogBuffers.clear()
            model.eventLogBuffers = model.eventLogBuffers + self.__log_ids
    def format(self):
        if len(self.__log_ids) <= 0:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.log\"\n'
        config += f'        android_log_config {{\n'
        for id in self.__log_ids:
            config += f'            log_ids: {id}\n'
        config += f'        }}\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        # 匹配 android_log_config 块
        log_config_pattern = r'android_log_config\s*\{([\s\S]*?)\}'
        log_config_matches = re.findall(log_config_pattern, config)

        for log_config in log_config_matches:
            # 在每个匹配的 android_log_config 块内寻找所有 log_ids
            log_ids_pattern = r'log_ids:\s*([A-Z0-9_]+)'
            log_ids_matches = re.findall(log_ids_pattern, log_config)
            # print(f'log_ids_matches={log_ids_matches}')
            for log_id_match in log_ids_matches:
                # 将匹配到的日志ID添加到列表中
                self.__log_ids.append(log_id_match)

class AndroidFrameTimeline:
    def __init__(self):
        self.__enableFrameTimeline = False
        pass
    def enableFrametimeLine(self):
        self.__enableFrameTimeline = True
    def syncToModel(self, model: Model):
        # print('syncToModel')
        if self.__enableFrameTimeline:
            model.enableFrameTimeline.set(1)
    def format(self):
        if not self.__enableFrameTimeline:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.surfaceflinger.frametimeline\"\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        frametimeline_match = re.search(r'name:\s*"android\.surfaceflinger\.frametimeline"', config)

        if frametimeline_match:
            self.enableFrametimeLine()

class AndroidGameInterventions:
    def __init__(self):
        self.__enableGameInterventions = False
        pass
    def enableGameInterventions(self):
        self.__enableGameInterventions = True
    def syncToModel(self, model: Model):
        # print('syncToModel')
        if self.__enableGameInterventions:
            model.enableGameInterventionList.set(1)
    def format(self):
        if not self.__enableGameInterventions:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.game_interventions\"\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取配置信息
        game_interventions_match = re.search(r'name:\s*"android\.game_interventions"', config)

        if game_interventions_match:
            self.enableGameInterventions()

class AndroidNetworkPackets:
    def __init__(self):
        self.__enable_network_packet_trace = False
        self.__network_packet_poll_interval: int = 0
        pass
    def enableNetworkPacketTrace(self):
        self.__enable_network_packet_trace = True
    def updateNetworkPacketPollInterval(self, interval: int):
        self.__network_packet_poll_interval = interval
    def syncToModel(self, model: Model):
        # print('syncToModel')
        if self.__enable_network_packet_trace:
            model.enableNetworkTracing.set(1)
        model.networkTracingInterval.set(self.__network_packet_poll_interval)
    def format(self):
        if not self.__enable_network_packet_trace:
            return ''
        if self.__network_packet_poll_interval <= 0:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"android.network_packets\"\n'
        config += f'        network_packet_trace_config {{\n'
        config += f'            poll_ms: {self.__network_packet_poll_interval}\n'
        config += f'        }}\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 正则表达式匹配整个网络数据包配置部分，包括 poll_ms 的值
        network_packets_pattern = r'name:\s*"android\.network_packets".*?network_packet_trace_config\s*\{[^}]*poll_ms:\s*(\d+)[^}]*\}'
        match = re.search(network_packets_pattern, config, re.DOTALL)

        if match:
            # 提取 poll_ms 的值
            poll_interval = int(match.group(1))
            self.enableNetworkPacketTrace()  # 启用网络数据包跟踪
            self.updateNetworkPacketPollInterval(poll_interval)  # 更新轮询间隔s

class LinuxPerf:
    def __init__(self):
        self.__frequency: int = 0
        self.__processes = []
        pass
    def setFrequency(self, freq: int):
        self.__frequency = freq
    def setProcessesCmdline(self, processes: str):
        cmdlines = split_and_filter_empty_lines(processes)
        for cmdline in cmdlines:
            if cmdline not in self.__processes:
                self.__processes.append(cmdline)
    def syncToModel(self, model: Model):
        # print('syncToModel')
        if self.__frequency > 0:
            model.enableCallstackSampling.set(1)
        model.callstackSamplingFreq.set(self.__frequency)
        if len(self.__processes) > 0:
            cmdlines = ''
            for process in self.__processes:
                cmdlines += f'{process}\n'
            model.callstackSamplingPrcesses.set(cmdlines[:-1])
    def format(self):
        if self.__frequency <= 0:
            return ''
        config  = f'data_sources: {{\n'
        config += f'    config {{\n'
        config += f'        name: \"linux.perf\"\n'
        config += f'        timebase  {{\n'
        config += f'            frequency: {self.__frequency}\n'
        config += f'            timestamp_clock: PERF_CLOCK_BOOTTIME\n'
        config += f'        }}\n'
        config += f'        callstack_sampling {{\n'
        config += f'            scope {{\n'
        for process in self.__processes:
            config += f'                target_cmdline: \"{process}\"\n'
        config += f'            }}\n'
        config += f'        }}\n'
        config += f'    }}\n'
        config += f'}}\n'
        return config
    def unformat(self, config: str):
        # 使用正则表达式提取频率和进程命令行
        frequency_match = re.search(r'frequency:\s*(\d+)', config)
        process_matches = re.findall(r'target_cmdline:\s*"(.*?)"', config)

        if frequency_match:
            self.setFrequency(int(frequency_match.group(1)))
        if process_matches:
            # print(f'LinuxPerf={process_matches}')
            self.__processes += process_matches

def split_and_filter_empty_lines(text: str):
    # 使用 splitlines() 分割字符串为行
    lines = text.splitlines()
    # 使用列表推导式过滤空行和空白行
    filtered_lines = [line for line in lines if line.strip()]    
    return filtered_lines

def defaultFrace():
    ftrace = LinuxFtrace()
    ftrace.addEvents('sched/sched_switch')
    ftrace.addEvents('power/suspend_resume')
    print(ftrace.format())
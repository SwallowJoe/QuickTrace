
from tkinter import *
from tkinter.ttk import *

class Model:

    def __init__(self):
        self.reset()
        pass
    def reset(self):
        # common
        self.__defaultRecordDurations = ['00:00:10','00:00:15','00:00:30',
                                       '00:01:00','00:05:00','00:30:00',
                                       '01:00:00','06:00:00','12:00:00']
        self.__defaultRecordDurations_seconds = convert_time_list_to_seconds(self.__defaultRecordDurations)
        self.recordingMode = IntVar()
        self.recordingMode.set(1) # stopWhenFull
        self.memoryBufferSize = IntVar()
        self.recordingDuration = StringVar()
        self.recordingDuration.set('00:00:10')
        self.recordProgressBarMax = IntVar()
        self.recordProgressBarCurrent = IntVar()
        # cpu
        self.__defaultPollIntervals = [250, 500, 1000, 2500, 5000, 30000, 60000]
        self.enableCpuUsageCounter = IntVar()
        self.cpuUsageCounterInterval = IntVar()
        self.cpuUsageCounterInterval.set(1000)
        self.enableCpuSchedulingDetails = IntVar()
        self.enableCpuFreq = IntVar()
        self.cpuFreqInterval = IntVar()
        self.cpuFreqInterval.set(1000)
        self.enableSyscalls = IntVar()
        # gpu
        self.enableGpuFreq = IntVar()
        self.enableGpuMemory = IntVar()
        self.enableGpuWorkPeriod = IntVar()
        # power
        self.enableBatteryDrain = IntVar()
        self.batteryDrainInterval = IntVar()
        self.batteryDrainInterval.set(1000)
        self.enableVoltages = IntVar()
        # memory
        # 22
        self.__defalutNativeHeapSamplingIntervals = [0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576]
        self.__defaultHeapDumpIntervals = [0, 1000, 10000, 30000, 60000, 300000, 600000, 1800000, 3600000]
        self.__defaultNativeHeapSharedMemBufs = [0, 8192,16384,32768,65536,131072,262144,524288,1048576,67108864,134217728,268435456,536870912]

        self.kernelMeminfoTags = ["active", "active_file", "active_anon", "anon_pages", "buffers", "cached", "cma_free", "cma_total", "commit_limit", "commited_as", "dirty", "gpu", "inactive", "inactive_anon", "inactive_file", "ion_heap", "ion_heap_pool", "kernel_stack", "mapped", "mem_available", "mem_free", "mem_total", "misc", "mlocked", "page_tables", "shmem", "slab", "slab_reclaimable", "slab_unreclaimable", "swap_cached", "swap_free", "swap_total", "unevictable", "vmalloc_chunk", "vmalloc_total", "vmalloc_used", "writeback", "zram"]

        self.enableNativeHeap = IntVar()
        self.nativeHeapProcessCmdlines = StringVar()
        self.nativeHeapSamplingInterval = IntVar()
        self.nativeHeapDumpsInterval = IntVar()
        self.nativeHeapDumpPhase = IntVar()
        self.nativeHeapSharedMemory = IntVar()
        self.enableBlockClient = IntVar()
        self.enableAllCustomAllocators = IntVar()

        self.enableJavaHeap = IntVar()
        self.javaHeapProcessCmdlines = StringVar()
        self.javaHeapDumpsInterval = IntVar()
        self.javaHeapDumpsPhase = IntVar()
        
        self.enableKernelMeminfo = IntVar()
        self.kernelMeminfoInterval = IntVar()
        self.kernelMeminfoCounters = []
        self.kernelMeminfoCountInfo = StringVar()
        self.kernelMeminfoCountInfo.set('Select counters (0):')

        self.enableHighFreqMemEvents = IntVar()
        self.enableLMK = IntVar()
        self.enablePerPorcessStats = IntVar()
        self.perProcessStatsInterval = IntVar()
        self.perProcessStatsInterval.set(1000)
        self.enableVirtualMemStats = IntVar()

        # Android Apps
        self.enableAtraceUserspaceAnnotations = IntVar()
        self.defaultAtraceCategories = {
            'Activity Manager': 'am',
            'ADB': 'adb',
            'AIDL calls':'aidl',
            'ART & Dalvik': 'dalvik',
            'Audio': 'audio',
            'Binder global lock trace': 'binder_lock',
            'Binder Kernel driver': 'binder_driver',
            'Bionic C library': 'bionic',
            'Camera': 'camera',
            'Database': 'database',
            'Graphics': 'gfx',
            'Hardware Modules': 'hal',
            'Input': 'input',
            'Network': 'network',
            'Neural Network API': 'nnapi',
            'Package Manager': 'pm',
            'Power Management': 'power',
            'RenderScript': 'rs',
            'Resource Loading': 'res',
            'Resource Overlay': 'rro',
            'Sync Manager': 'sm',
            'System Server': 'ss',
            'Vibrator': 'vibrator',
            'Video': 'video',
            'View System': 'view',
            'WebView': 'webview',
            'Window Manager': 'wm',
        }
        self.atraceCategories = []
        self.atraceProcesses = StringVar()
        self.enableRecordAllApps = IntVar()

        self.enableEventLog = IntVar()
        self.eventLogIds = {
            'Binary events': 'LID_EVENTS',
            'Crash': 'LID_CRASH',
            'kernel': 'LID_KERNEL',
            'Main': 'LID_DEFAULT',
            'Radio': 'LID_RADIO',
            'Security': 'LID_SECURITY',
            'Stats': 'LID_STATS',
            'System': 'LID_SYSTEM',
        }
        self.eventLogBuffers = []
        self.enableFrameTimeline = IntVar()
        self.enableGameInterventionList = IntVar()
        self.enableNetworkTracing = IntVar()
        self.defaultNetworkTracingIntervals = [100, 250, 500, 1000, 2500]
        self.networkTracingInterval = IntVar()

        # Stack Samples
        self.enableCallstackSampling = IntVar()
        self.defaultCallstackSamplingFreq = [20,40,60,80,100,120,140,160,180,200]
        self.callstackSamplingFreq = IntVar()
        self.callstackSamplingPrcesses = StringVar()
        # command
        self.commandBuffer = StringVar()
        pass

    ##### Record Settings #####
    def updateRecordDuration(self, index):
        if index < 0 or index > 9:
            return
        self.recordingDuration.set(self.__defaultRecordDurations[index])
    def getRecordDurationIndex(self):
        # print(f'recordDuration={self.recordingDuration.get()}')
        return theNearestIndexRoundOf(self.__defaultRecordDurations_seconds, time_to_seconds(self.recordingDuration.get()))
    ###### CPU #####
    def updateCpuUsageCounterInterval(self, index):
        if index < 0 or index > 7:
            return
        self.cpuUsageCounterInterval.set(self.__defaultPollIntervals[index])
    def getCpuUsageCounterIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultPollIntervals, self.cpuUsageCounterInterval.get())

    def updateCpuFreqInterval(self, index):
        if index < 0 or index > 7:
            return
        self.cpuFreqInterval.set(self.__defaultPollIntervals[index])
    def getCpuFreqIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultPollIntervals, self.cpuFreqInterval.get())
    ###### power ######
    def updateBatteryDrainInterval(self, index):
        if index < 0 or index > 7:
            return
        self.batteryDrainInterval.set(self.__defaultPollIntervals[index])
    def getBatteryDrainIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultPollIntervals, self.batteryDrainInterval.get())
    ####### memory ######
    def updateNativeHeapProcessCmdlines(self, cmdlines: str):
        self.nativeHeapProcessCmdlines.set(cmdlines)
    def updateNativeHeapSamplingInterval(self, index):
        if index < 0 or index >= len(self.__defalutNativeHeapSamplingIntervals):
            return
        self.nativeHeapSamplingInterval.set(self.__defalutNativeHeapSamplingIntervals[index])
    def getNativeHeapSamplingIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defalutNativeHeapSamplingIntervals, self.nativeHeapSamplingInterval.get())

    def updateNativeHeapDumpsInterval(self, index):
        if index < 0 or index > 8:
            return
        self.nativeHeapDumpsInterval.set(self.__defaultHeapDumpIntervals[index])
    def getNativeHeapDumpsIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultHeapDumpIntervals, self.nativeHeapDumpsInterval.get())

    def updateNativeHeapDumpPhase(self, index):
        if index < 0 or index > 8:
            return
        self.nativeHeapDumpPhase.set(self.__defaultHeapDumpIntervals[index])
    def getNativeHeapDumpPhaseIndex(self):
        return theNearestIndexRoundOf(self.__defaultHeapDumpIntervals, self.nativeHeapDumpPhase.get())

    def updateNativeHeapSharedMemBufs(self, index):
        # 0~12
        if index < 0 or index >= len(self.__defaultNativeHeapSharedMemBufs):
            return
        self.nativeHeapSharedMemory.set(self.__defaultNativeHeapSharedMemBufs[index])
    def getNativeHeapSharedMemBufsIndex(self):
        return theNearestIndexRoundOf(self.__defaultNativeHeapSharedMemBufs, self.nativeHeapSharedMemory.get())
    def updateJavaHeapProcessCmdlines(self, cmdlines: str):
        self.javaHeapProcessCmdlines.set(cmdlines)
    def updateJavaHeapDumpsInterval(self, index):
        if index < 0 or index > 8:
            return
        self.javaHeapDumpsInterval.set(self.__defaultHeapDumpIntervals[index])
    def getJavaHeapDumpsIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultHeapDumpIntervals, self.javaHeapDumpsInterval.get())
    def updateJavaHeapDumpsPhase(self, index):
        if index < 0 or index > 8:
            return
        self.javaHeapDumpsPhase.set(self.__defaultHeapDumpIntervals[index])
    def getJavaHeapDumpsPhaseIndex(self):
        return theNearestIndexRoundOf(self.__defaultHeapDumpIntervals, self.javaHeapDumpsPhase.get())
    def updateKernelMeminfoInterval(self, index):
        if index < 0 or index > 7:
            return
        self.kernelMeminfoInterval.set(self.__defaultPollIntervals[index])
    def getKernelMeminfoIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultPollIntervals, self.kernelMeminfoInterval.get())
    def updateKernelMeminfoCounters(self, countersList):
        self.kernelMeminfoCounters.clear()
        self.kernelMeminfoCounters = self.kernelMeminfoCounters + countersList
        self.kernelMeminfoCountInfo.set(f'Select counters ({len(self.kernelMeminfoCounters)}):')
    def updatePerProcessStats(self, index):
        if index < 0 or index > 7:
            return
        self.perProcessStatsInterval.set(self.__defaultPollIntervals[index])
    def getPerProcessStatsIntervalIndex(self):
        return theNearestIndexRoundOf(self.__defaultPollIntervals, self.perProcessStatsInterval.get())
    ################## APP ####################
    def updateAtraceCategories(self, atraceCategories):
        self.atraceCategories.clear()
        self.atraceCategories = self.atraceCategories + atraceCategories
    def updateAtraceProcesses(self, processes: str):
        self.atraceProcesses.set(processes)
    def udpateEventLogBuffers(self, eventLogBuffers):
        self.eventLogBuffers.clear()
        for event in eventLogBuffers:
            self.eventLogBuffers.append(self.eventLogIds[event])
    def updateNetworkTracingInterval(self, index):
        if index < 0 or index > 4:
            return
        self.networkTracingInterval.set(self.defaultNetworkTracingIntervals[index])
    def getNetworkTracingIntervalIndex(self):
        return theNearestIndexRoundOf(self.defaultNetworkTracingIntervals, self.networkTracingInterval.get())
    ############## Callstack ########c
    def updateCallstackSamplingFreq(self, index):
        if index < 0 or index > 9:
            return
        self.callstackSamplingFreq.set(self.defaultCallstackSamplingFreq[index])
    def getCallstackSamplingFreqIndex(self):
        return theNearestIndexRoundOf(self.defaultCallstackSamplingFreq, self.callstackSamplingFreq.get())
    def updateCallstackSamplingProcesses(self, processes: str):
        self.callstackSamplingPrcesses.set(processes)
    
def theNearestIndexRoundOf(values, target):
    # 初始化最小差值和最接近的索引
    min_diff = float('inf')
    nearest_index = -1
    
    # 遍历数组中的每个值
    for index, value in enumerate(values):
        # 计算当前值与目标值的差的绝对值
        current_diff = abs(value - target)
        
        # 如果当前差的绝对值小于最小差值，则更新最小差值和最接近的索引
        if current_diff < min_diff:
            min_diff = current_diff
            nearest_index = index
    
    return nearest_index

def convert_time_list_to_seconds(time_list):
    seconds_list = []
    for time_str in time_list:
        # 将时间字符串 'HH:MM:SS' 转换为秒数
        seconds_list.append(time_to_seconds(time_str))
    return seconds_list

def time_to_seconds(time_str):
    # 将时间字符串 'HH:MM:SS' 转换为秒数
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

import os
import glob
import subprocess
import _thread as thread
import time
from datetime import datetime
import tkinter
import tkinter.messagebox
from command import CommandGenerator
from ui import Win
import adb_commands
from model import Model

class Controller:
    ui: Win

    def __init__(self):
        pass

    def init(self, ui):
        self.ui = ui
        
        # 标记开始拖动时的索引
        self.__kernelMeminfo_start_index = None
        self.__atrace_start_index = None
        self.__eventlog_start_index = None

        self.model: Model = ui.model
        self.commandGenerator = CommandGenerator(self.model)
        self.selectedDevice = ''
        self.onDirInit()
        self.onMainUiInit()
        self.onUiInit()
        eventThreadStart(self)
    def syncCommand(self, config_path: str):
        print(f'sync command {config_path}')
        config_content = read_file(config_path)
        print(f'config_content={config_content}')
        self.commandGenerator.syncCommand(config_content)
        self.onUiInit()

    def onSlideMemoryBufferSize(self, value):
        # print("onSlideMemoryBufferSize ", value)
        self.model.memoryBufferSize.set(1 << round(float(value)))
    def onSlideDuration(self, value):
        index = round(float(value))
        self.model.updateRecordDuration(index)
    def onKernelMeminfoItemSelected(self,evt):
        # print("<<ListboxSelect>>事件未处理:",evt)
        pass
    def openFileDiretory(self,evt):
        # 获取当前脚本的绝对路径
        # 使用subprocess模块打开资源管理器并定位到指定目录
        subprocess.run(['explorer', self.traces_dir])
    def onUiInit(self):
        # print("Ui初始化")
        self.onCommonUiInit()
        self.onCpuUiInit()
        self.onGpuUiInit()
        self.onPowerUiInit()
        self.onMemoryUiInit()
        self.onAppsUiInit()
        self.onStackSamplesUiInit()
        self.onCommandUiInit()
    def onMainUiInit(self):
        # print("onMainUiInit")
        self.updateDeviceList()
        self.updateConfigList()
    def onCommonUiInit(self):
        # print("onCommonUiInit")

        if self.model.recordingMode == 1:
            self.ui.tk_radio_button_stopWhenFull.invoke()
        elif self.model.recordingMode == 2:
            self.ui.tk_radio_button_ringBuffer.invoke()
        memory_index = self.model.memoryBufferSize.get().bit_length() - 1
        # print(f'index={memory_index} memoryBufferSize={self.model.memoryBufferSize.get()}')
        self.ui.tk_scale_memoryBufferSize.set(memory_index)
        duration_index = self.model.getRecordDurationIndex()
        self.ui.tk_scale_duration.set(duration_index)

    def onCpuUiInit(self):
        # print("onCpuUiInit")
        self.onHandleEnableCpuUsageCounter(tkinter.NORMAL)
        self.onHandleEnableCpuFreq(tkinter.NORMAL)

        self.ui.tk_scale_cpuUsageInterval.set(self.model.getCpuUsageCounterIntervalIndex())
        self.ui.tk_scale_cpuFreqInterval.set(self.model.getCpuFreqIntervalIndex())

        self.onHandleEnableCpuUsageCounter(getUiState(self.model.enableCpuUsageCounter))
        self.onHandleEnableCpuFreq(getUiState(self.model.enableCpuFreq))
    def handleEnableCpuUsageCounter(self):
        self.onHandleEnableCpuUsageCounter(getUiState(self.model.enableCpuUsageCounter))
    def onHandleEnableCpuUsageCounter(self, uiState):
        self.ui.tk_scale_cpuUsageInterval.config(state=uiState)
        self.ui.tk_input_cpuUsageInterval.config(state=uiState)
    def handleEnableCpuFreq(self):
        self.onHandleEnableCpuFreq(getUiState(self.model.enableCpuFreq))
    def onHandleEnableCpuFreq(self, uiState):
        self.ui.tk_scale_cpuFreqInterval.config(state=uiState)
        self.ui.tk_input_cpuFreqInterval.config(state=uiState)
        
    def onSlideCpuUsageInterval(self, value):
        index = round(float(value))
        self.model.updateCpuUsageCounterInterval(index)
    def onSlideCpuFreqInterval(self, value):
        index = round(float(value))
        self.model.updateCpuFreqInterval(index)

    def onGpuUiInit(self):
        # print("onGpuUiInit")
        pass

    def onPowerUiInit(self):
        # print("onPowerUiInit")
        self.onHandleEnableBatteryDrain(uiState = tkinter.NORMAL)
        self.ui.tk_scale_batteryDrainInterval.set(self.model.getBatteryDrainIntervalIndex())
        self.onHandleEnableBatteryDrain(uiState = getUiState(self.model.enableBatteryDrain))
    def onSlideBatteryDrainInterval(self, value):
        index = round(float(value))
        self.model.updateBatteryDrainInterval(index)
    def handleEnableBatteryDrain(self):
        self.onHandleEnableBatteryDrain(uiState = getUiState(self.model.enableBatteryDrain))
    def onHandleEnableBatteryDrain(self, uiState):
        # print(f'handleEnableBatteryDrain {self.model.enableBatteryDrain.get()}')
        self.ui.tk_scale_batteryDrainInterval.config(state=uiState)
        self.ui.tk_input_batteryDrainInterval.config(state=uiState)

    def onMemoryUiInit(self):
        # print("onMemoryUiInit")
        self.onHandleEnableNativeHeap(uiState = tkinter.NORMAL)
        self.onHandleEnableJavaHeap(uiState = tkinter.NORMAL)
        self.onHandleEnableKernelMeminfo(uiState = tkinter.NORMAL)
        self.onHandleEnablePerProcessStats(uiState = tkinter.NORMAL)

        self.ui.tk_scale_nativeHeapSamplingInterval.set(self.model.getNativeHeapSamplingIntervalIndex())
        self.ui.tk_scale_nativeHeapDumpsInterval.set(self.model.getNativeHeapDumpsIntervalIndex())
        self.ui.tk_scale_nativeHeapDumpPhase.set(self.model.getNativeHeapDumpPhaseIndex())
        self.ui.tk_scale_nativeHeapMemoryBuffer.set(self.model.getNativeHeapSharedMemBufsIndex())
        self.ui.tk_scale_perProcessStatsInterval.set(self.model.getPerProcessStatsIntervalIndex())
        self.ui.tk_text_nativeHeapProcessList.delete('1.0', tkinter.END)
        # print(f'nativeHeapProcessCmdlines={self.model.nativeHeapProcessCmdlines.get()}')
        self.ui.tk_text_nativeHeapProcessList.insert(1.0, self.model.nativeHeapProcessCmdlines.get())
        self.onHandleEnableNativeHeap(uiState = getUiState(self.model.enableNativeHeap))

        self.ui.tk_scale_javaHeapInterval.set(self.model.getJavaHeapDumpsIntervalIndex())
        self.ui.tk_scale_javaHeapDumpsPhase.set(self.model.getJavaHeapDumpsPhaseIndex())
        self.ui.tk_text_javaHeapProcessList.delete('1.0', tkinter.END)
        self.ui.tk_text_javaHeapProcessList.insert(1.0, self.model.javaHeapProcessCmdlines.get())

        self.onHandleEnableJavaHeap(uiState = getUiState(self.model.enableJavaHeap))

        # 根据selected_items中的字符串选中Listbox中的对应项
        resetItemUiOfListbox(self.ui.tk_list_box_kernelMeminfoCounter)
        for counter in self.model.kernelMeminfoCounters:
            # 找到项的索引，然后设置选中状态
            for index in range(self.ui.tk_list_box_kernelMeminfoCounter.size()):
                if self.ui.tk_list_box_kernelMeminfoCounter.get(index).lower() in counter.lower():
                    self.ui.tk_list_box_kernelMeminfoCounter.selection_set(index)
                    configItemUiOfListbox(self.ui.tk_list_box_kernelMeminfoCounter, index)
        count = len(self.ui.tk_list_box_kernelMeminfoCounter.curselection())
        self.ui.tk_label_kernelMeminfoSelectCounters.config(text=f'Select counters ({count}/{self.ui.tk_list_box_kernelMeminfoCounter.size()}):')

        self.ui.tk_scale_kernelMeminfoInterval.set(self.model.getKernelMeminfoIntervalIndex())
        self.onHandleEnableKernelMeminfo(uiState = getUiState(self.model.enableKernelMeminfo))

        self.ui.tk_scale_perProcessStatsInterval.set(self.model.getPerProcessStatsIntervalIndex())
        self.onHandleEnablePerProcessStats(uiState = getUiState(self.model.enablePerPorcessStats))
    def onSlideNativeHeapSamplingInterval(self, value):
        index = round(float(value))
        self.model.updateNativeHeapSamplingInterval(index)
    def onSlideNativeHeapDumpsInterval(self, value):
        index = round(float(value))
        self.model.updateNativeHeapDumpsInterval(index)
    def onSlideNativeHeapDumpPhase(self, value):
        index = round(float(value))
        self.model.updateNativeHeapDumpPhase(index)
    def onSlideNativeHeapSharedMemBufs(self, value):
        index = round(float(value))
        self.model.updateNativeHeapSharedMemBufs(index)
    def handleEnableNativeHeap(self):
        self.onHandleEnableNativeHeap(uiState = getUiState(self.model.enableNativeHeap))
    def onHandleEnableNativeHeap(self, uiState):
        #self.ui.tk_scale_batteryDrainInterval.config(state=uiState)
        #self.ui.tk_input_batteryDrainInterval.config(state=uiState)
        self.ui.tk_scale_nativeHeapSamplingInterval.config(state=uiState)
        self.ui.tk_input_nativeHeapSamplingInterval.config(state=uiState)
        self.ui.tk_scale_nativeHeapDumpsInterval.config(state=uiState)
        self.ui.tk_input_nativeHeapDumpsInterval.config(state=uiState)
        self.ui.tk_scale_nativeHeapDumpPhase.config(state=uiState)
        self.ui.tk_input_nativeHeapDumpPhase.config(state=uiState)
        self.ui.tk_scale_nativeHeapMemoryBuffer.config(state=uiState)
        self.ui.tk_input_nativeHeapMemoryBuffer.config(state=uiState)
        self.ui.tk_check_button_nativeHeapBlockClient.config(state=uiState)
        self.ui.tk_check_button_nativeHeapCustomAllocators.config(state=uiState)
        self.ui.tk_text_nativeHeapProcessList.config(state=uiState)

    def onSlideJavaHeapDumpsInterval(self, value):
        index = round(float(value))
        self.model.updateJavaHeapDumpsInterval(index)
    def onSlideJavaHeapDumpsPhase(self, value):
        index = round(float(value))
        self.model.updateJavaHeapDumpsPhase(index)
    def handleEnableJavaHeap(self):
        self.onHandleEnableJavaHeap(uiState = getUiState(self.model.enableJavaHeap))
    def onHandleEnableJavaHeap(self, uiState):
        self.ui.tk_scale_javaHeapInterval.config(state=uiState)
        self.ui.tk_input_javaHeapInterval.config(state=uiState)
        self.ui.tk_scale_javaHeapDumpsPhase.config(state=uiState)
        self.ui.tk_input_javaHeapDumpsPhase.config(state=uiState)

    def handleEnableKernelMeminfo(self):
        self.onHandleEnableKernelMeminfo(uiState = getUiState(self.model.enableKernelMeminfo))

    def onHandleEnableKernelMeminfo(self, uiState):
        self.ui.tk_scale_kernelMeminfoInterval.config(state=uiState)
        self.ui.tk_input_kernelMeminfoInterval.config(state=uiState)
        self.ui.tk_list_box_kernelMeminfoCounter.config(state=uiState)
    def onSlideKernelMeminfoInterval(self, value):
        index = round(float(value))
        self.model.updateKernelMeminfoInterval(index)
    def handleEnablePerProcessStats(self):
        self.onHandleEnablePerProcessStats(uiState = getUiState(self.model.enablePerPorcessStats))

    def onHandleEnablePerProcessStats(self, uiState):
        self.ui.tk_scale_perProcessStatsInterval.config(state=uiState)
        self.ui.tk_input_perProcessStatsInterval.config(state=uiState)
    def onSlidePerProcessStats(self, value):
        index = round(float(value))
        self.model.updatePerProcessStats(index)

    def onAppsUiInit(self):
        # print("onAppsUiInit")
        self.onHandleEnableAtrace(uiState = tkinter.NORMAL)
        self.onHandleEnableRecordAllApps(uiState = tkinter.NORMAL)
        self.onHandleEnableEventLog(uiState = tkinter.NORMAL)
        #self.onHandleEnableFrameTimeline()
        #self.onHandleEnableGameInterventions()
        self.onHandleEnableNetworkTracing(uiState = tkinter.NORMAL)

        self.ui.tk_text_atraceProcessList.delete('1.0', tkinter.END)
        self.ui.tk_text_atraceProcessList.insert(1.0, self.model.atraceProcesses.get())
        self.ui.tk_scale_networkTracingInterval.set(self.model.getNetworkTracingIntervalIndex())

        # 根据selected_items中的字符串选中Listbox中的对应项
        # print(f'atraceCategories={self.model.atraceCategories}')
        resetItemUiOfListbox(self.ui.tk_list_box_atrace)
        for category in self.model.atraceCategories:
            # 找到项的索引，然后设置选中状态
            matching_keys = [key for key, value in self.model.defaultAtraceCategories.items() if value == category]
            if matching_keys:                
                for index in range(self.ui.tk_list_box_atrace.size()):
                    if self.ui.tk_list_box_atrace.get(index).lower() in matching_keys[0].lower():
                        self.ui.tk_list_box_atrace.selection_set(index)
                        configItemUiOfListbox(self.ui.tk_list_box_atrace, index)
        count = len(self.ui.tk_list_box_atrace.curselection())        
        self.ui.tk_label_atraceCategories.config(text=f'Enables c++/Java codebase annotations ({count}/{self.ui.tk_list_box_atrace.size()}):')

        # 根据selected_items中的字符串选中Listbox中的对应项
        # print(f'eventLogBuffers={self.model.eventLogBuffers}')
        resetItemUiOfListbox(self.ui.tk_list_box_eventLog)
        for event in self.model.eventLogBuffers:
            # 找到项的索引，然后设置选中状态
            matching_keys = [key for key, value in self.model.eventLogIds.items() if value == event]
            if matching_keys:
                for index in range(self.ui.tk_list_box_eventLog.size()):
                    if self.ui.tk_list_box_eventLog.get(index).lower() in matching_keys[0].lower():
                        self.ui.tk_list_box_eventLog.selection_set(index)
                        configItemUiOfListbox(self.ui.tk_list_box_eventLog, index)
        count = len(self.ui.tk_list_box_eventLog.curselection())
        self.ui.tk_label_eventlog.config(text=f'Streams the event log into the trace({count}/{self.ui.tk_list_box_eventLog.size()}):')

        self.onHandleEnableAtrace(uiState = getUiState(self.model.enableAtraceUserspaceAnnotations))
        self.onHandleEnableRecordAllApps(uiState = getUiState(self.model.enableRecordAllApps))
        self.onHandleEnableEventLog(uiState = getUiState(self.model.enableEventLog))
        self.onHandleEnableFrameTimeline()
        self.onHandleEnableGameInterventions()
        self.onHandleEnableNetworkTracing(uiState = getUiState(self.model.enableNetworkTracing))
    def handleEnableAtrace(self):
        self.onHandleEnableAtrace(uiState = getUiState(self.model.enableAtraceUserspaceAnnotations))
    def onHandleEnableAtrace(self, uiState):
        self.ui.tk_list_box_atrace.config(state=uiState)
    def handleEnableRecordAllApps(self):
        self.onHandleEnableRecordAllApps(uiState = getUiState(self.model.enableRecordAllApps))
    def onHandleEnableRecordAllApps(self, uiState):
        self.ui.tk_text_atraceProcessList.config(state=uiState)
    def handleEnableEventLog(self):
        self.onHandleEnableEventLog(uiState = getUiState(self.model.enableEventLog))
    def onHandleEnableEventLog(self, uiState):
        self.ui.tk_list_box_eventLog.config(state=uiState)
    def handleEnableFrameTimeline(self):
        self.onHandleEnableFrameTimeline()
    def onHandleEnableFrameTimeline(self):
        pass
    def handleEnableGameInterventions(self):
        self.onHandleEnableGameInterventions()
    def onHandleEnableGameInterventions(self):
        pass
    def handleEnableNetworkTracing(self):
        self.onHandleEnableNetworkTracing(uiState = getUiState(self.model.enableNetworkTracing))
    def onHandleEnableNetworkTracing(self, uiState):
        self.ui.tk_scale_networkTracingInterval.config(state=uiState)
        self.ui.tk_input_networkTracingInterval.config(state=uiState)
    def onSlideNetworkTracingInterval(self, value):
        index = round(float(value))
        self.model.updateNetworkTracingInterval(index)

    def onStackSamplesUiInit(self):
        # print("onStackSamplesUiInit")
        self.onHandleEnableCallstackSampling(uiState = tkinter.NORMAL)

        self.ui.tk_text_callstackSamplingProcessList.delete('1.0', tkinter.END)
        self.ui.tk_text_callstackSamplingProcessList.insert(1.0, self.model.callstackSamplingPrcesses.get())
        self.ui.tk_scale_callstackSamplingFreq.set(self.model.getCallstackSamplingFreqIndex())

        self.onHandleEnableCallstackSampling(uiState = getUiState(self.model.enableCallstackSampling))
    def handleEnableCallstackSampling(self):
        self.onHandleEnableCallstackSampling(uiState = getUiState(self.model.enableCallstackSampling))
    def onHandleEnableCallstackSampling(self, uiState):
        self.ui.tk_scale_callstackSamplingFreq.config(state=uiState)
        self.ui.tk_input_callstackSamplingFreq.config(state=uiState)
        self.ui.tk_text_callstackSamplingProcessList.config(state=uiState)
    def onSlideCallstackSamplingFreq(self, value):
        index = round(float(value))
        self.model.updateCallstackSamplingFreq(index)

    def onCommandUiInit(self):
        # print("onCommandUiInit")
        self.__genConfigs()
        pass
    def onDirInit(self):
        # print("目录初始化")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建子目录的完整路径
        self.traces_dir = os.path.join(self.script_dir, 'traces')
        # 检查子目录是否存在，如果不存在则创建
        if not os.path.exists(self.traces_dir):
            os.makedirs(self.traces_dir)
        # 构建子目录的完整路径
        self.configs_dir = os.path.join(self.script_dir, 'configs')
        # 检查子目录是否存在，如果不存在则创建
        if not os.path.exists(self.configs_dir):
            os.makedirs(self.configs_dir)
    def updateDeviceList(self):
        # print("更新连接设备列表")
        # 设备列表选项
        deviceStr = adb_commands.deviceList()
        if len(deviceStr) == 0:
            self.ui.tk_select_box_devices['values'] = ("等待设备连接...")
            self.ui.tk_select_box_devices.current(0)
            self.selectedDevice = self.ui.tk_select_box_devices.get()
            return 0
        deviceList = deviceStr.splitlines()
        self.ui.tk_select_box_devices['values'] = deviceList
        if len(self.selectedDevice) == 0:
            self.ui.tk_select_box_devices.current(0)
            self.selectedDevice = self.ui.tk_select_box_devices.get()

        if deviceStr.find(self.selectedDevice) == -1:
            self.ui.tk_select_box_devices.current(0)
            self.selectedDevice = self.ui.tk_select_box_devices.get()
            
        # 遍历Combobox的值
        for value in self.ui.tk_select_box_devices['values']:
            # 如果项包含指定字符，则选中该项并退出循环
            if self.selectedDevice in value:
                self.ui.tk_select_box_devices.current(self.ui.tk_select_box_devices['values'].index(value))
                break
        # print("window update... ", len(self.ui.tk_select_box_devices['values']))
        return 1
    def updateConfigList(self):
        # print("updateConfigList: ", self.configs_dir)
        configList = getFileNameListOf(self.configs_dir, "*.config")
        # print("Config files found:")
        # for file in configList:
        #    print(file)
        # 使用 replace() 去除前缀
        configNameList = [os.path.basename(s) for s in configList]
        self.ui.tk_select_box_configs['values'] = configNameList
        if (len(configNameList) > 0):
            for value in self.ui.tk_select_box_configs['values']:
                if 'custom.config' in value:
                    self.ui.tk_select_box_configs.current(self.ui.tk_select_box_configs['values'].index(value))
                    break
                else:
                    self.ui.tk_select_box_configs.current(0)

    def onTabChangeOfProbes(self, event):
        # 获取当前选中的选项卡索引
        current_index = event.widget.index("current")
        # print(f"当前选中的选项卡索引是: {current_index}")
        if current_index == 7: # command
            self.model.updateNativeHeapProcessCmdlines(self.ui.tk_text_nativeHeapProcessList.get('1.0', 'end-1c'))
            self.model.updateJavaHeapProcessCmdlines(self.ui.tk_text_javaHeapProcessList.get('1.0', 'end-1c'))
            self.model.updateAtraceProcesses(self.ui.tk_text_atraceProcessList.get('1.0', 'end-1c'))
            self.model.updateCallstackSamplingProcesses(self.ui.tk_text_callstackSamplingProcessList.get('1.0', 'end-1c'))
            self.__genConfigs()

    def __genConfigs(self):
        command = self.commandGenerator.generateCommand()

        self.ui.tk_text_command.config(state=tkinter.NORMAL)
        self.ui.tk_text_command.delete(1.0, tkinter.END)
        self.ui.tk_text_command.insert(1.0, command)
        self.ui.tk_text_command.config(state=tkinter.DISABLED)
        return command

    def on_listbox_kernelmeminfo_press(self, listbox: tkinter.Listbox, event):
        # 获取当前点击的位置
        resetItemUiOfListbox(listbox)
        self.__kernelMeminfo_start_index = listbox.nearest(event.y)
        
    def on_listbox_kernelmeminfo_drag(self, listbox: tkinter.Listbox,event):
        # 获取当前鼠标指针所在行的索引
        index = listbox.nearest(event.y)
        # 如果鼠标左键按下
        if event.state & 1:
            # 如果有开始拖动的索引
            if self.__kernelMeminfo_start_index is not None:
                # 选中从开始拖动的索引到当前索引之间的所有项
                if index >= self.__kernelMeminfo_start_index:
                    for i in range(self.____kernelMeminfo_start_index, index + 1):
                        listbox.select_set(i)
                else:
                    for i in range(index, self.__kernelMeminfo_start_index + 1):
                        listbox.select_set(i)
        # 获取所有选中项的索引
        selected_indices = listbox.curselection()
        # 使用索引来获取选中的项目
        self.model.updateKernelMeminfoCounters([listbox.get(i) for i in selected_indices])
        self.ui.tk_label_kernelMeminfoSelectCounters.config(text=f'Select counters ({len(selected_indices)}/listbox.size()):')

    def on_listbox_atrace_press(self, listbox: tkinter.Listbox, event):
        # 获取当前点击的位置
        resetItemUiOfListbox(listbox)
        self.__atrace_start_index = listbox.nearest(event.y)
        
    def on_listbox_atrace_drag(self, listbox: tkinter.Listbox,event):
        # 获取当前鼠标指针所在行的索引
        index = listbox.nearest(event.y)
        # 如果鼠标左键按下
        if event.state & 1:
            # 如果有开始拖动的索引
            if self.__atrace_start_index is not None:
                # 选中从开始拖动的索引到当前索引之间的所有项
                if index >= self.__atrace_start_index:
                    for i in range(self.__atrace_start_index, index + 1):
                        listbox.select_set(i)
                else:
                    for i in range(index, self.__atrace_start_index + 1):
                        listbox.select_set(i)
        # 获取所有选中项的索引
        selected_indices = listbox.curselection()
        # 使用索引来获取选中的项目
        self.model.updateAtraceCategories([listbox.get(i) for i in selected_indices])
        self.ui.tk_label_atraceCategories.config(text=f'Enables c++/Java codebase annotations ({len(selected_indices)}/{listbox.size()}):')

    def on_listbox_eventlog_press(self, listbox: tkinter.Listbox, event):
        # 获取当前点击的位置
        resetItemUiOfListbox(listbox)
        self.__eventlog_start_index = listbox.nearest(event.y)

    def on_listbox_eventlog_drag(self, listbox: tkinter.Listbox, event):
        # 获取当前鼠标指针所在行的索引
        index = listbox.nearest(event.y)
        # 如果鼠标左键按下
        if event.state & 1:
            # 如果有开始拖动的索引
            if self.__eventlog_start_index is not None:
                # 选中从开始拖动的索引到当前索引之间的所有项
                if index >= self.__eventlog_start_index:
                    for i in range(self.__eventlog_start_index, index + 1):
                        listbox.select_set(i)
                else:
                    for i in range(index, self.__eventlog_start_index + 1):
                        listbox.select_set(i)
        # 获取所有选中项的索引
        selected_indices = listbox.curselection()
        # 使用索引来获取选中的项目
        self.model.udpateEventLogBuffers([listbox.get(i) for i in selected_indices])
        self.ui.tk_label_eventlog.config(text=f'Streams the event log into the trace({len(selected_indices)}/{listbox.size()}):')

    def recordTrace(self,evt):
        if self.selectedDevice == '等待设备连接...':
            tkinter.messagebox.showinfo("提示", "请选择抓取trace的设备!!!")
            return
        config = self.__genConfigs()
        # print(f'recordTrace:\n{config}\n')
        configFile = self.__wirteToRecordingConfig(config)
        now = datetime.now()
        traceName = now.strftime("%Y%m%d-%H%M%S")
        traceFile = os.path.join(self.traces_dir, traceName)
        adb_commands.recordPerfettoTrace(traceFile, self.selectedDevice, configFile)
        self.__updateProcessBar()
        # traceName['text']='Trace名: ' + os.getcwd() +'\\'+ lastTraceName + ".html"
    def __updateProcessBar(self):
        # 分解 duration 字符串
        hours, minutes, seconds = map(int, self.model.recordingDuration.get().split(':'))
        # ms
        duration = (hours * 3600 + minutes * 60 + seconds) * 1000
        self.ui.tk_progressbar_recording['maximum'] = 100

        def update_progress(progress_bar, duration: float):
            # 设置初始进度为0
            progress = 0
            interval = duration / 100.0
            # 更新进度条的循环
            while progress <= 100:
                # 更新进度条的值
                progress += 1
                progress_bar['value'] = progress
        
                self.ui.tk_button_record.config(text=f'正在抓取({(duration - progress * 100)/1000}s)...', state=tkinter.NORMAL)
                # 更新GUI
                self.ui.update()
                time.sleep(interval / 1000.0)  # ms
            self.ui.tk_button_record.config(text=f'抓取 trace', state=tkinter.NORMAL)

        newThreadStart(update_progress, self.ui.tk_progressbar_recording, duration)
        self.ui.tk_button_record.config(text=f'正在抓取 trace, 请等待...', state=tkinter.DISABLED)

    def __wirteToRecordingConfig(self, config: str):
        # 打开文件并写入内容
        recordingConfig = os.path.join(self.configs_dir, 'recording.tmp')
        # 检查文件是否存在，如果不存在则创建
        with open(recordingConfig, "w", encoding="utf-8") as file:
            file.write(config)
        return recordingConfig
    def clearTraces(self, evt):
        print("clear all cached traces. ")
        html_files = glob.glob(os.path.join(self.traces_dir, '*.html'))
        # 删除这些文件
        for file_path in html_files:
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Error: {e}")
    def on_trace_config_select(self, evt):
        # 获取选中的项的文本
        selected_item = self.ui.tk_select_box_configs.get()
        # 在控制台输出选中的项
        # print("Selected item:", selected_item)
        self.syncCommand(os.path.join(self.configs_dir, selected_item))
    def saveCurrentConfig(self, evt):
        configName = self.ui.tk_select_box_configs.get()
        print(f'saveCurrentConfig={configName}')
        # 打开文件并写入内容
        recordingConfig = os.path.join(self.configs_dir, configName)
        # 检查文件是否存在，如果不存在则创建
        with open(recordingConfig, "w", encoding="utf-8") as file:
            file.write(self.__genConfigs())
        pass
    def newConfig(self, evt):
        print('newConfig')
        config_name = tkinter.StringVar()
        # 创建弹窗
        top = tkinter.Toplevel(self.ui)
        top.title("新Trace配置")

        # 设置弹窗的大小和位置
        top.geometry("300x100+300+300")

        # 创建一个Label作为输入框的说明
        label = tkinter.Label(top, text="请输入配置名称:")
        label.pack(side=tkinter.TOP, pady=(10, 0))

        # 创建一个Entry用于输入
        entry = tkinter.Entry(top, width=50, textvariable=config_name)
        entry.pack(side=tkinter.TOP, pady=(0, 10))

        def on_confirm():
            print(f'on_confirm={config_name.get()}')
            configName = f'{config_name.get()}.config'
            # 打开文件并写入内容
            recordingConfig = os.path.join(self.configs_dir, configName)
            # 检查文件是否存在，如果不存在则创建
            with open(recordingConfig, "w", encoding="utf-8") as file:
                file.write('')
            # configList = self.ui.tk_select_box_configs['values']
            # 获取当前的值列表
            current_values = self.ui.tk_select_box_configs['values']
            # 添加新项
            self.ui.tk_select_box_configs['values'] = list(current_values) + [configName]
            self.ui.tk_select_box_configs.set(configName)
            top.destroy()
        # 创建一个确认按钮
        confirm_button = tkinter.Button(top, text="确认", command=on_confirm)
        confirm_button.pack(side=tkinter.RIGHT, padx=(0, 10))

        # 创建一个取消按钮
        def on_cancel():
            print(f'on_cancel={config_name.get()}')
            top.destroy()
        cancel_button = tkinter.Button(top, text="取消", command=on_cancel)
        cancel_button.pack(side=tkinter.RIGHT)

        # 运行弹窗的事件循环
        top.mainloop()

def configItemUiOfListbox(listbox: tkinter.Listbox, index):
    listbox.itemconfigure(index, {'bg': 'lightblue', 'fg': 'black'})    
def resetItemUiOfListbox(listbox: tkinter.Listbox):
    for index in range(listbox.size()):
        listbox.itemconfigure(index, {'bg': 'white', 'fg': 'black'})   

def getUiState(value: tkinter.IntVar):
    if value.get() == 1:
        return tkinter.NORMAL
    else:
        return tkinter.DISABLED

def threadMainLooper(threadName, delay, window):
    while delay>0:
        time.sleep(delay)
        window.updateDeviceList()

def eventThreadStart(window):
    try:
        thread.start_new_thread(threadMainLooper, ("EventThread", 2, window, ))
    except:
        print("Error: unable to start thread")

def funcThreadMainLooper(callback, args):
    callback(*args)


def newThreadStart(callback, *args):
    try:
        thread.start_new_thread(funcThreadMainLooper, (callback, args))
    except:
        print("Error: unable to start thread")


def getFileNameListOf(directory, submix):
    # 使用glob模块和通配符查找所有以'submix'结尾的文件
    config_files = glob.glob(os.path.join(directory, submix))
    return config_files

def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return ''
    except Exception as e:
        print(f"An error occurred: {e}")
        return ''

import random
from tkinter import *
from tkinter.ttk import *
from model import Model

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.model = Model()
        self.tk_tabs_probes = self.__tk_tabs_probes(self)
        self.tk_label_frame_recordingMode = self.__tk_label_frame_recordingMode( self.tk_tabs_probes_0)
        self.tk_scale_memoryBufferSize = self.__tk_scale_memoryBufferSize( self.tk_label_frame_recordingMode) 
        self.tk_label_memoryBufferSize = self.__tk_label_memoryBufferSize( self.tk_label_frame_recordingMode) 
        self.tk_input_memoryBufferSize = self.__tk_input_memoryBufferSize( self.tk_label_frame_recordingMode) 
        self.tk_label_MB = self.__tk_label_MB( self.tk_label_frame_recordingMode) 
        self.tk_label_duration_title = self.__tk_label_duration_title( self.tk_label_frame_recordingMode) 
        self.tk_scale_duration = self.__tk_scale_duration( self.tk_label_frame_recordingMode) 
        self.tk_input_duration = self.__tk_input_duration( self.tk_label_frame_recordingMode) 
        self.tk_label_duration = self.__tk_label_duration( self.tk_label_frame_recordingMode) 
        self.tk_radio_button_stopWhenFull = self.__tk_radio_button_stopWhenFull( self.tk_label_frame_recordingMode) 
        self.tk_radio_button_ringBuffer = self.__tk_radio_button_ringBuffer( self.tk_label_frame_recordingMode) 
        self.tk_check_button_cpuUsageCounter = self.__tk_check_button_cpuUsageCounter( self.tk_tabs_probes_1)
        self.tk_scale_cpuUsageInterval = self.__tk_scale_cpuUsageInterval( self.tk_tabs_probes_1)
        self.tk_label_cpuUsageIntervalTitle = self.__tk_label_cpuUsageIntervalTitle( self.tk_tabs_probes_1)
        self.tk_input_cpuUsageInterval = self.__tk_input_cpuUsageInterval( self.tk_tabs_probes_1)
        self.tk_label_cpuUsageInterval = self.__tk_label_cpuUsageInterval( self.tk_tabs_probes_1)
        self.tk_scale_cpuFreqInterval = self.__tk_scale_cpuFreqInterval( self.tk_tabs_probes_1)
        self.tk_label_cpuFreqIntervalTitle = self.__tk_label_cpuFreqIntervalTitle( self.tk_tabs_probes_1)
        self.tk_input_cpuFreqInterval = self.__tk_input_cpuFreqInterval( self.tk_tabs_probes_1)
        self.tk_label_cpuFreqInterval = self.__tk_label_cpuFreqInterval( self.tk_tabs_probes_1)

        self.tk_check_button_schedulingDetails = self.__tk_check_button_schedulingDetails( self.tk_tabs_probes_1)
        self.tk_check_button_cpuFreq = self.__tk_check_button_cpuFreq( self.tk_tabs_probes_1)
        self.tk_check_button_syscalls = self.__tk_check_button_syscalls( self.tk_tabs_probes_1)
        self.tk_check_button_gpuFreq = self.__tk_check_button_gpuFreq( self.tk_tabs_probes_2)
        self.tk_check_button_gpuMemory = self.__tk_check_button_gpuMemory( self.tk_tabs_probes_2)
        self.tk_check_button_gpuWorkPeriod = self.__tk_check_button_gpuWorkPeriod( self.tk_tabs_probes_2)
        self.tk_check_button_bettaryDrain = self.__tk_check_button_bettaryDrain( self.tk_tabs_probes_3)
        self.tk_label_batteryDrain = self.__tk_label_batteryDrain( self.tk_tabs_probes_3)
        self.tk_input_batteryDrainInterval = self.__tk_input_batteryDrainInterval( self.tk_tabs_probes_3)
        self.tk_label_batteryDrainInterval = self.__tk_label_batteryDrainInterval( self.tk_tabs_probes_3)
        self.tk_scale_batteryDrainInterval = self.__tk_scale_batteryDrainInterval( self.tk_tabs_probes_3)
        self.tk_check_button_voltages = self.__tk_check_button_voltages( self.tk_tabs_probes_3)
        self.tk_tabs_memory = self.__tk_tabs_memory( self.tk_tabs_probes_4)
        self.tk_label_nativeHeapProcessList = self.__tk_label_nativeHeapProcessList( self.tk_tabs_memory_0)
        self.tk_check_button_nativeHeapProfiling = self.__tk_check_button_nativeHeapProfiling( self.tk_tabs_memory_0)
        self.tk_label_nativeHeapSamplingInterval = self.__tk_label_nativeHeapSamplingInterval( self.tk_tabs_memory_0)
        self.tk_scale_nativeHeapSamplingInterval = self.__tk_scale_nativeHeapSamplingInterval( self.tk_tabs_memory_0)
        self.tk_input_nativeHeapSamplingInterval = self.__tk_input_nativeHeapSamplingInterval( self.tk_tabs_memory_0)
        self.tk_label_lyy3blp0 = self.__tk_label_lyy3blp0( self.tk_tabs_memory_0)
        self.tk_label_lyy3cdfp = self.__tk_label_lyy3cdfp( self.tk_tabs_memory_0)
        self.tk_scale_nativeHeapDumpsInterval = self.__tk_scale_nativeHeapDumpsInterval( self.tk_tabs_memory_0)
        self.tk_input_nativeHeapDumpsInterval = self.__tk_input_nativeHeapDumpsInterval( self.tk_tabs_memory_0)
        self.tk_label_lyy3f9tj = self.__tk_label_lyy3f9tj( self.tk_tabs_memory_0)
        self.tk_label_lyy3iutb = self.__tk_label_lyy3iutb( self.tk_tabs_memory_0)
        self.tk_scale_nativeHeapDumpPhase = self.__tk_scale_nativeHeapDumpPhase( self.tk_tabs_memory_0)
        self.tk_input_nativeHeapDumpPhase = self.__tk_input_nativeHeapDumpPhase( self.tk_tabs_memory_0)
        self.tk_label_lyy3wdbf = self.__tk_label_lyy3wdbf( self.tk_tabs_memory_0)
        self.tk_label_lyy3wwix = self.__tk_label_lyy3wwix( self.tk_tabs_memory_0)
        self.tk_scale_nativeHeapMemoryBuffer = self.__tk_scale_nativeHeapMemoryBuffer( self.tk_tabs_memory_0)
        self.tk_input_nativeHeapMemoryBuffer = self.__tk_input_nativeHeapMemoryBuffer( self.tk_tabs_memory_0)
        self.tk_label_lyy4azd6 = self.__tk_label_lyy4azd6( self.tk_tabs_memory_0)
        self.tk_check_button_nativeHeapBlockClient = self.__tk_check_button_nativeHeapBlockClient( self.tk_tabs_memory_0)
        self.tk_check_button_nativeHeapCustomAllocators = self.__tk_check_button_nativeHeapCustomAllocators( self.tk_tabs_memory_0)
        self.tk_check_button_javaHeapDumps = self.__tk_check_button_javaHeapDumps( self.tk_tabs_memory_1)
        self.tk_text_javaHeapProcessList = self.__tk_text_javaHeapProcessList( self.tk_tabs_memory_1)
        self.tk_text_nativeHeapProcessList = self.__tk_text_nativeHeapProcessList( self.tk_tabs_memory_0)
        self.tk_label_lyy4v9nl = self.__tk_label_lyy4v9nl( self.tk_tabs_memory_1)
        self.tk_label_lyy4wmmr = self.__tk_label_lyy4wmmr( self.tk_tabs_memory_1)
        self.tk_scale_javaHeapInterval = self.__tk_scale_javaHeapInterval( self.tk_tabs_memory_1)
        self.tk_input_javaHeapInterval = self.__tk_input_javaHeapInterval( self.tk_tabs_memory_1)
        self.tk_label_lyy50wfb = self.__tk_label_lyy50wfb( self.tk_tabs_memory_1)
        self.tk_label_lyy52asz = self.__tk_label_lyy52asz( self.tk_tabs_memory_1)
        self.tk_scale_javaHeapDumpsPhase = self.__tk_scale_javaHeapDumpsPhase( self.tk_tabs_memory_1)
        self.tk_input_javaHeapDumpsPhase = self.__tk_input_javaHeapDumpsPhase( self.tk_tabs_memory_1)
        self.tk_label_lyy57tn3 = self.__tk_label_lyy57tn3( self.tk_tabs_memory_1)
        self.tk_list_box_kernelMeminfoCounter = self.__tk_list_box_kernelMeminfoCounter( self.tk_tabs_memory_2)
        self.tk_check_button_kernelMeminfo = self.__tk_check_button_kernelMeminfo( self.tk_tabs_memory_2)
        self.tk_label_lyy5gxb2 = self.__tk_label_lyy5gxb2( self.tk_tabs_memory_2)
        self.tk_scale_kernelMeminfoInterval = self.__tk_scale_kernelMeminfoInterval( self.tk_tabs_memory_2)
        self.tk_input_kernelMeminfoInterval = self.__tk_input_kernelMeminfoInterval( self.tk_tabs_memory_2)
        self.tk_label_lyy5iolj = self.__tk_label_lyy5iolj( self.tk_tabs_memory_2)
        self.tk_label_kernelMeminfoSelectCounters = self.__tk_label_kernelMeminfoSelectCounters( self.tk_tabs_memory_2)
        self.tk_check_button_record_per_process = self.__tk_check_button_record_per_process( self.tk_tabs_memory_2)
        self.tk_label_lyy68ydk = self.__tk_label_lyy68ydk( self.tk_tabs_memory_2)
        self.tk_scale_perProcessStatsInterval = self.__tk_scale_perProcessStatsInterval( self.tk_tabs_memory_2)
        self.tk_input_perProcessStatsInterval = self.__tk_input_perProcessStatsInterval( self.tk_tabs_memory_2)
        self.tk_label_lyy6n3e1 = self.__tk_label_lyy6n3e1( self.tk_tabs_memory_2)
        self.tk_check_button_memoryEvent = self.__tk_check_button_memoryEvent( self.tk_tabs_probes_4)
        self.tk_check_button_lmk = self.__tk_check_button_lmk( self.tk_tabs_probes_4)
        self.tk_text_command = self.__tk_text_command( self.tk_tabs_probes_7)
        self.tk_tabs_androidApps = self.__tk_tabs_androidApps( self.tk_tabs_probes_5)
        self.tk_check_button_atrace = self.__tk_check_button_atrace( self.tk_tabs_androidApps_0)
        self.tk_label_atraceCategories = self.__tk_label_atraceCategories( self.tk_tabs_androidApps_0)
        self.tk_list_box_atrace = self.__tk_list_box_atrace( self.tk_tabs_androidApps_0)
        self.tk_check_button_atraceForAllApps = self.__tk_check_button_atraceForAllApps( self.tk_tabs_androidApps_0)
        self.tk_text_atraceProcessList = self.__tk_text_atraceProcessList( self.tk_tabs_androidApps_0)
        self.tk_check_button_eventLog = self.__tk_check_button_eventLog( self.tk_tabs_androidApps_1)
        self.tk_label_eventlog = self.__tk_label_eventlog( self.tk_tabs_androidApps_1)
        self.tk_list_box_eventLog = self.__tk_list_box_eventLog( self.tk_tabs_androidApps_1)
        self.tk_frame_lyy7nkbb = self.__tk_frame_lyy7nkbb( self.tk_tabs_androidApps_1)
        self.tk_check_button_frameTimeline = self.__tk_check_button_frameTimeline( self.tk_frame_lyy7nkbb) 
        self.tk_check_button_gameMode = self.__tk_check_button_gameMode( self.tk_frame_lyy7nkbb) 
        self.tk_check_button_networkTracing = self.__tk_check_button_networkTracing( self.tk_frame_lyy7nkbb) 
        self.tk_label_lyy7txma = self.__tk_label_lyy7txma( self.tk_frame_lyy7nkbb) 
        self.tk_scale_networkTracingInterval = self.__tk_scale_networkTracingInterval( self.tk_frame_lyy7nkbb) 
        self.tk_input_networkTracingInterval = self.__tk_input_networkTracingInterval( self.tk_frame_lyy7nkbb) 
        self.tk_label_lyy7w4tw = self.__tk_label_lyy7w4tw( self.tk_frame_lyy7nkbb) 
        self.tk_check_button_callstackSampling = self.__tk_check_button_callstackSampling( self.tk_tabs_probes_6)
        self.tk_label_lyy80jsb = self.__tk_label_lyy80jsb( self.tk_tabs_probes_6)
        self.tk_label_lyy82gfv = self.__tk_label_lyy82gfv( self.tk_tabs_probes_6)
        self.tk_scale_callstackSamplingFreq = self.__tk_scale_callstackSamplingFreq( self.tk_tabs_probes_6)
        self.tk_input_callstackSamplingFreq = self.__tk_input_callstackSamplingFreq( self.tk_tabs_probes_6)
        self.tk_label_lyy84hai = self.__tk_label_lyy84hai( self.tk_tabs_probes_6)
        self.tk_label_lyy85oyw = self.__tk_label_lyy85oyw( self.tk_tabs_probes_6)
        self.tk_text_callstackSamplingProcessList = self.__tk_text_callstackSamplingProcessList( self.tk_tabs_probes_6)
        self.tk_label_device = self.__tk_label_device(self)
        self.tk_select_box_devices = self.__tk_select_box_devices(self)
        self.tk_button_record = self.__tk_button_record(self)
        self.tk_button_openFileDir = self.__tk_button_openFileDir(self)
        self.tk_button_clearTraces = self.__tk_button_clearTraces(self)
        self.tk_select_box_configs = self.__tk_select_box_configs(self)
        self.tk_button_save_config_as = self.__tk_button_save_config_as(self)
        self.tk_button_new_config = self.__tk_button_new_config(self)
        self.tk_progressbar_recording = self.__tk_progressbar_recording(self)
    def __win(self):
        self.title("QuickTrace - V1.0_by Joseph.Huang")
        # 设置窗口大小、居中
        width = 800
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.iconphoto(True, PhotoImage(file='ic_launcher.png'))
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_tabs_probes(self,parent):
        frame = Notebook(parent)
        self.tk_tabs_probes_0 = self.__tk_frame_probes_0(frame)
        frame.add(self.tk_tabs_probes_0, text="常规配置")
        self.tk_tabs_probes_1 = self.__tk_frame_probes_1(frame)
        frame.add(self.tk_tabs_probes_1, text="CPU")
        self.tk_tabs_probes_2 = self.__tk_frame_probes_2(frame)
        frame.add(self.tk_tabs_probes_2, text="GPU")
        self.tk_tabs_probes_3 = self.__tk_frame_probes_3(frame)
        frame.add(self.tk_tabs_probes_3, text="Power")
        self.tk_tabs_probes_4 = self.__tk_frame_probes_4(frame)
        frame.add(self.tk_tabs_probes_4, text="Memory")
        self.tk_tabs_probes_5 = self.__tk_frame_probes_5(frame)
        frame.add(self.tk_tabs_probes_5, text="Apps")
        self.tk_tabs_probes_6 = self.__tk_frame_probes_6(frame)
        frame.add(self.tk_tabs_probes_6, text="Stack Samples")
        self.tk_tabs_probes_7 = self.__tk_frame_probes_7(frame)
        frame.add(self.tk_tabs_probes_7, text="配置命令")
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_0(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_1(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_2(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_3(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_4(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_5(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_6(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_frame_probes_7(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=76, width=761, height=514)
        return frame
    def __tk_label_frame_recordingMode(self,parent):
        frame = LabelFrame(parent,text="Recording Mode",)
        frame.place(x=18, y=20, width=715, height=280)
        return frame
    def __tk_scale_memoryBufferSize(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=2, to=9, command=self.ctl.onSlideMemoryBufferSize,)
        scale.place(x=24, y=55, width=528, height=30)
        return scale
    def __tk_label_memoryBufferSize(self,parent):
        label = Label(parent,text="In-memory Buffer Size:",anchor="center", )
        label.place(x=23, y=20, width=149, height=30)
        return label
    def __tk_input_memoryBufferSize(self,parent):
        ipt = Entry(parent, textvariable=self.model.memoryBufferSize)
        ipt.place(x=566, y=56, width=96, height=30)
        return ipt
    def __tk_label_MB(self,parent):
        label = Label(parent,text="MB",anchor="center", )
        label.place(x=665, y=56, width=30, height=30)
        return label
    def __tk_label_duration_title(self,parent):
        label = Label(parent,text="Max duration:",anchor="center", )
        label.place(x=24, y=103, width=95, height=30)
        return label
    def __tk_scale_duration(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=8, command=self.ctl.onSlideDuration,)
        scale.place(x=24, y=145, width=528, height=30)
        return scale
    def __tk_input_duration(self,parent):
        ipt = Entry(parent, textvariable=self.model.recordingDuration)
        ipt.place(x=566, y=145, width=98, height=30)
        return ipt
    def __tk_label_duration(self,parent):
        label = Label(parent,text="h:m:s",anchor="center", )
        label.place(x=665, y=145, width=37, height=30)
        return label
    def __tk_radio_button_stopWhenFull(self,parent):
        rb = Radiobutton(parent,text="Stop When Full",variable=self.model.recordingMode,value=1)
        rb.place(x=26, y=218, width=119, height=30)
        return rb
    def __tk_radio_button_ringBuffer(self,parent):
        rb = Radiobutton(parent,text="Ring buffer",variable=self.model.recordingMode,value=2)
        rb.place(x=167, y=218, width=95, height=30)
        return rb
    def __tk_check_button_cpuUsageCounter(self,parent):
        cb = Checkbutton(parent,text="Corase CPU usage counter",onvalue=1,offvalue=0,variable=self.model.enableCpuUsageCounter,command=self.ctl.handleEnableCpuUsageCounter)
        cb.place(x=20, y=36, width=190, height=30)
        return cb
    def __tk_scale_cpuUsageInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=6, command=self.ctl.onSlideCpuUsageInterval)
        scale.place(x=342, y=36, width=228, height=30)
        return scale
    def __tk_label_cpuUsageIntervalTitle(self,parent):
        label = Label(parent,text="Poll Interval:",anchor="center", )
        label.place(x=238, y=36, width=87, height=30)
        return label
    def __tk_input_cpuUsageInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.cpuUsageCounterInterval)
        ipt.place(x=581, y=36, width=124, height=30)
        return ipt
    def __tk_label_cpuUsageInterval(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=712, y=36, width=30, height=30)
        return label
    def __tk_check_button_schedulingDetails(self,parent):
        cb = Checkbutton(parent,text="Scheduling details",onvalue=1,offvalue=0,variable=self.model.enableCpuSchedulingDetails,)
        cb.place(x=20, y=104, width=135, height=30)
        return cb
    def __tk_check_button_cpuFreq(self,parent):
        cb = Checkbutton(parent,text="CPU Frequency and idle states",onvalue=1,offvalue=0,variable=self.model.enableCpuFreq,command=self.ctl.handleEnableCpuFreq,)
        cb.place(x=22, y=165, width=200, height=30)
        return cb
    def __tk_scale_cpuFreqInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=6, command=self.ctl.onSlideCpuFreqInterval)
        scale.place(x=342, y=165, width=228, height=30)
        return scale
    def __tk_label_cpuFreqIntervalTitle(self,parent):
        label = Label(parent,text="Poll Interval:",anchor="center", )
        label.place(x=238, y=165, width=87, height=30)
        return label
    def __tk_input_cpuFreqInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.cpuFreqInterval)
        ipt.place(x=581, y=165, width=124, height=30)
        return ipt
    def __tk_label_cpuFreqInterval(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=712, y=165, width=30, height=30)
        return label
    def __tk_check_button_syscalls(self,parent):
        cb = Checkbutton(parent,text="Syscalls",onvalue=1,offvalue=0,variable=self.model.enableSyscalls,)
        cb.place(x=20, y=230, width=88, height=30)
        return cb
    def __tk_check_button_gpuFreq(self,parent):
        cb = Checkbutton(parent,text="GPU frequency",onvalue=1,offvalue=0,variable=self.model.enableGpuFreq,)
        cb.place(x=60, y=52, width=127, height=30)
        return cb
    def __tk_check_button_gpuMemory(self,parent):
        cb = Checkbutton(parent,text="GPU memory",onvalue=1,offvalue=0,variable=self.model.enableGpuMemory,)
        cb.place(x=58, y=134, width=127, height=30)
        return cb
    def __tk_check_button_gpuWorkPeriod(self,parent):
        cb = Checkbutton(parent,text="GPU work period",onvalue=1,offvalue=0,variable=self.model.enableGpuWorkPeriod,)
        cb.place(x=58, y=218, width=141, height=30)
        return cb
    def __tk_check_button_bettaryDrain(self,parent):
        cb = Checkbutton(parent,text="Battery drain & power rails",onvalue=1,offvalue=0,variable=self.model.enableBatteryDrain,command=self.ctl.handleEnableBatteryDrain,)
        cb.place(x=40, y=40, width=220, height=30)
        return cb
    def __tk_label_batteryDrain(self,parent):
        label = Label(parent,text="Poll interval:",anchor="center", )
        label.place(x=287, y=40, width=99, height=30)
        return label
    def __tk_input_batteryDrainInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.batteryDrainInterval)
        ipt.place(x=587, y=40, width=96, height=30)
        return ipt
    def __tk_label_batteryDrainInterval(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=685, y=40, width=30, height=30)
        return label
    def __tk_scale_batteryDrainInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=6, command=self.ctl.onSlideBatteryDrainInterval)
        scale.place(x=398, y=40, width=179, height=30)
        return scale
    def __tk_check_button_voltages(self,parent):
        cb = Checkbutton(parent,text="Board voltages & frequencies",onvalue=1,offvalue=0,variable=self.model.enableVoltages)
        cb.place(x=40, y=140, width=220, height=30)
        return cb
    def __tk_tabs_memory(self,parent):
        frame = Notebook(parent)
        self.tk_tabs_memory_0 = self.__tk_frame_memory_0(frame)
        frame.add(self.tk_tabs_memory_0, text="Native heap profiling")
        self.tk_tabs_memory_1 = self.__tk_frame_memory_1(frame)
        frame.add(self.tk_tabs_memory_1, text="Java heap dumps")
        self.tk_tabs_memory_2 = self.__tk_frame_memory_2(frame)
        frame.add(self.tk_tabs_memory_2, text="Other options")
        frame.place(x=20, y=50, width=720, height=427)
        return frame
    def __tk_frame_memory_0(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=50, width=720, height=427)
        return frame
    def __tk_frame_memory_1(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=50, width=720, height=427)
        return frame
    def __tk_frame_memory_2(self,parent):
        frame = Frame(parent)
        frame.place(x=20, y=50, width=720, height=427)
        return frame
    def __tk_label_nativeHeapProcessList(self,parent):
        label = Label(parent,text="Names or pids of the processes to track:",anchor="center", )
        label.place(x=10, y=50, width=244, height=30)
        return label
    def __tk_check_button_nativeHeapProfiling(self,parent):
        cb = Checkbutton(parent,text="Enable native heap profiling",onvalue=1,offvalue=0,variable=self.model.enableNativeHeap,command=self.ctl.handleEnableNativeHeap,)
        cb.place(x=10, y=10, width=189, height=30)
        return cb
    def __tk_label_nativeHeapSamplingInterval(self,parent):
        label = Label(parent,text="Sampling interval:",anchor="center", )
        label.place(x=280, y=10, width=120, height=30)
        return label
    def __tk_scale_nativeHeapSamplingInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0,to=21,command=self.ctl.onSlideNativeHeapSamplingInterval,)
        scale.place(x=280, y=50, width=290, height=30)
        return scale
    def __tk_input_nativeHeapSamplingInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.nativeHeapSamplingInterval)
        ipt.place(x=580, y=50, width=100, height=30)
        return ipt
    def __tk_label_lyy3blp0(self,parent):
        label = Label(parent,text="B",anchor="center", )
        label.place(x=680, y=50, width=30, height=30)
        return label
    def __tk_label_lyy3cdfp(self,parent):
        label = Label(parent,text="Continuous dumps interval(time between following dumps):",anchor="center", )
        label.place(x=280, y=85, width=360, height=30)
        return label
    def __tk_scale_nativeHeapDumpsInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=8, command=self.ctl.onSlideNativeHeapDumpsInterval,)
        scale.place(x=280, y=125, width=290, height=30)
        return scale
    def __tk_input_nativeHeapDumpsInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.nativeHeapDumpsInterval,)
        ipt.place(x=580, y=125, width=100, height=30)
        return ipt
    def __tk_label_lyy3f9tj(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=680, y=125, width=30, height=30)
        return label
    def __tk_label_lyy3iutb(self,parent):
        label = Label(parent,text="Continuous dumps phase(time before fist dump):",anchor="center", )
        label.place(x=280, y=165, width=305, height=30)
        return label
    def __tk_scale_nativeHeapDumpPhase(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=8, command=self.ctl.onSlideNativeHeapDumpPhase,)
        scale.place(x=280, y=205, width=290, height=30)
        return scale
    def __tk_input_nativeHeapDumpPhase(self,parent):
        ipt = Entry(parent, textvariable=self.model.nativeHeapDumpPhase)
        ipt.place(x=580, y=205, width=100, height=30)
        return ipt
    def __tk_label_lyy3wdbf(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=680, y=205, width=30, height=30)
        return label
    def __tk_label_lyy3wwix(self,parent):
        label = Label(parent,text="Shared memory buffer:",anchor="center", )
        label.place(x=280, y=240, width=151, height=30)
        return label
    def __tk_scale_nativeHeapMemoryBuffer(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0,to=12,command=self.ctl.onSlideNativeHeapSharedMemBufs)
        scale.place(x=280, y=280, width=290, height=30)
        return scale
    def __tk_input_nativeHeapMemoryBuffer(self,parent):
        ipt = Entry(parent, textvariable=self.model.nativeHeapSharedMemory)
        ipt.place(x=580, y=280, width=100, height=30)
        return ipt
    def __tk_label_lyy4azd6(self,parent):
        label = Label(parent,text="B",anchor="center", )
        label.place(x=680, y=280, width=30, height=30)
        return label
    def __tk_check_button_nativeHeapBlockClient(self,parent):
        cb = Checkbutton(parent,text="Block client",onvalue=1,offvalue=0,variable=self.model.enableBlockClient,)
        cb.place(x=280, y=333, width=150, height=30)
        return cb
    def __tk_check_button_nativeHeapCustomAllocators(self,parent):
        cb = Checkbutton(parent,text="All custom allocators(Q+)",onvalue=1,offvalue=0,variable=self.model.enableAllCustomAllocators,)
        cb.place(x=479, y=332, width=180, height=30)
        return cb
    def __tk_check_button_javaHeapDumps(self,parent):
        cb = Checkbutton(parent,text="Enable java heap dumps",onvalue=1,offvalue=0,variable=self.model.enableJavaHeap,command=self.ctl.handleEnableJavaHeap,)
        cb.place(x=10, y=10, width=160, height=30)
        return cb
    def __tk_text_javaHeapProcessList(self,parent):
        text = Text(parent)
        text.place(x=10, y=90, width=250, height=300)
        return text
    def __tk_text_nativeHeapProcessList(self,parent):
        frame = Frame(parent,)
        frame.place(x=10, y=90, width=250, height=300)

        scrollbar_v = Scrollbar(frame)
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h = Scrollbar(frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        text = Text(frame, yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set,wrap=NONE,)
        text.place(x=0, y=0, width=225, height=285)
        return text
    def __tk_label_lyy4v9nl(self,parent):
        label = Label(parent,text="Names or pids the processes to track:",anchor="center", )
        label.place(x=10, y=50, width=240, height=30)
        return label
    def __tk_label_lyy4wmmr(self,parent):
        label = Label(parent,text="Continuous dumps interval(time between following dumps):",anchor="center", )
        label.place(x=300, y=100, width=360, height=30)
        return label
    def __tk_scale_javaHeapInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=8, command=self.ctl.onSlideJavaHeapDumpsInterval,)
        scale.place(x=300, y=150, width=270, height=30)
        return scale
    def __tk_input_javaHeapInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.javaHeapDumpsInterval,)
        ipt.place(x=585, y=150, width=100, height=30)
        return ipt
    def __tk_label_lyy50wfb(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=685, y=150, width=30, height=30)
        return label
    def __tk_label_lyy52asz(self,parent):
        label = Label(parent,text="Continuous dumps phase(time before first dump):",anchor="center", )
        label.place(x=300, y=225, width=305, height=30)
        return label
    def __tk_scale_javaHeapDumpsPhase(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=8, command=self.ctl.onSlideJavaHeapDumpsPhase,)
        scale.place(x=300, y=270, width=270, height=30)
        return scale
    def __tk_input_javaHeapDumpsPhase(self,parent):
        ipt = Entry(parent, textvariable=self.model.javaHeapDumpsPhase,)
        ipt.place(x=585, y=270, width=100, height=30)
        return ipt
    def __tk_label_lyy57tn3(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=685, y=270, width=30, height=30)
        return label
    def __tk_list_box_kernelMeminfoCounter(self,parent):
        lb = Listbox(parent, selectmode=EXTENDED,)
        for tag in self.model.kernelMeminfoTags:
            lb.insert(END, tag)
        lb.place(x=11, y=172, width=279, height=221)
        return lb
    def __tk_check_button_kernelMeminfo(self,parent):
        cb = Checkbutton(parent,text="Enable kernel meminfo",onvalue=1,offvalue=0,variable=self.model.enableKernelMeminfo,command=self.ctl.handleEnableKernelMeminfo,)
        cb.place(x=10, y=10, width=180, height=30)
        return cb
    def __tk_label_lyy5gxb2(self,parent):
        label = Label(parent,text="Poll interval(polling of /proc/meminfo):",anchor="center", )
        label.place(x=12, y=52, width=237, height=30)
        return label
    def __tk_scale_kernelMeminfoInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=6, command=self.ctl.onSlideKernelMeminfoInterval,)
        scale.place(x=10, y=97, width=170, height=30)
        return scale
    def __tk_input_kernelMeminfoInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.kernelMeminfoInterval)
        ipt.place(x=189, y=98, width=80, height=30)
        return ipt
    def __tk_label_lyy5iolj(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=270, y=98, width=30, height=30)
        return label
    def __tk_label_kernelMeminfoSelectCounters(self,parent):
        label = Label(parent,text="Select counters (0):",anchor="center", )
        label.place(x=10, y=130, width=140, height=30)
        return label
    def __tk_check_button_record_per_process(self,parent):
        cb = Checkbutton(parent,text="Record per process stats",onvalue=1,offvalue=0,variable=self.model.enablePerPorcessStats,)
        cb.place(x=325, y=10, width=180, height=30)
        return cb
    def __tk_label_lyy68ydk(self,parent):
        label = Label(parent,text="Poll interval:",anchor="center", )
        label.place(x=325, y=52, width=88, height=30)
        return label
    def __tk_scale_perProcessStatsInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=6, command=self.ctl.onSlidePerProcessStats,)
        scale.place(x=325, y=97, width=170, height=30)
        return scale
    def __tk_input_perProcessStatsInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.perProcessStatsInterval,)
        ipt.place(x=510, y=97, width=100, height=30)
        return ipt
    def __tk_label_lyy6n3e1(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=612, y=97, width=30, height=30)
        return label
    def __tk_check_button_memoryEvent(self,parent):
        cb = Checkbutton(parent,text="High-frequency memory events",onvalue=1,offvalue=0,variable=self.model.enableHighFreqMemEvents)
        cb.place(x=21, y=10, width=208, height=30)
        return cb
    def __tk_check_button_lmk(self,parent):
        cb = Checkbutton(parent,text="Low memory killer",onvalue=1,offvalue=0,variable=self.model.enableLMK,)
        cb.place(x=354, y=10, width=170, height=30)
        return cb
    def __tk_text_command(self,parent):
        scrollbar_v = Scrollbar(parent)
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h = Scrollbar(parent, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        text = Text(parent, background="black", foreground="white", yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set,wrap=NONE,)
        text.place(x=8, y=6, width=730, height=466)
        return text
    def __tk_tabs_androidApps(self,parent):
        frame = Notebook(parent)
        self.tk_tabs_androidApps_0 = self.__tk_frame_androidApps_0(frame)
        frame.add(self.tk_tabs_androidApps_0, text="Atrace userspace annotations")
        self.tk_tabs_androidApps_1 = self.__tk_frame_androidApps_1(frame)
        frame.add(self.tk_tabs_androidApps_1, text="Other options")
        frame.place(x=11, y=22, width=736, height=455)
        return frame
    def __tk_frame_androidApps_0(self,parent):
        frame = Frame(parent)
        frame.place(x=11, y=22, width=736, height=455)
        return frame
    def __tk_frame_androidApps_1(self,parent):
        frame = Frame(parent)
        frame.place(x=11, y=22, width=736, height=455)
        return frame
    def __tk_check_button_atrace(self,parent):
        cb = Checkbutton(parent,text="Enable atrace userspace annotations",onvalue=1,offvalue=0,variable=self.model.enableAtraceUserspaceAnnotations,command=self.ctl.handleEnableAtrace)
        cb.place(x=10, y=10, width=260, height=30)
        return cb
    def __tk_label_atraceCategories(self,parent):
        label = Label(parent,text="Enables c++/Java codebase annotations (0):",anchor="center", )
        label.place(x=10, y=50, width=290, height=30)
        return label
    def __tk_list_box_atrace(self,parent):
        lb = Listbox(parent, selectmode=EXTENDED,)
        
        for key, value in self.model.defaultAtraceCategories.items():
            lb.insert(END, key)
        
        lb.place(x=10, y=90, width=243, height=330)
        return lb
    def __tk_check_button_atraceForAllApps(self,parent):
        cb = Checkbutton(parent,text="Record events from all Android apps and services",onvalue=0,offvalue=1,variable=self.model.enableRecordAllApps,command=self.ctl.handleEnableRecordAllApps)
        cb.place(x=330, y=90, width=320, height=30)
        return cb
    def __tk_text_atraceProcessList(self,parent):
        frame = Frame(parent,)
        frame.place(x=330, y=138, width=390, height=280)

        scrollbar_v = Scrollbar(frame)
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h = Scrollbar(frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        text = Text(frame, yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set,wrap=NONE,)
        text.place(x=0, y=0, width=370, height=260)
        return text
    def __tk_check_button_eventLog(self,parent):
        cb = Checkbutton(parent,text="Enable event log",onvalue=1,offvalue=0,variable=self.model.enableEventLog,command=self.ctl.handleEnableEventLog,)
        cb.place(x=10, y=10, width=140, height=30)
        return cb
    def __tk_label_eventlog(self,parent):
        label = Label(parent,text="Streams the event log into the trace(0):",anchor="center", )
        label.place(x=10, y=50, width=255, height=30)
        return label
    def __tk_list_box_eventLog(self,parent):
        lb = Listbox(parent, selectmode=EXTENDED,)
        for key, value in self.model.eventLogIds.items():
            lb.insert(END, key)        
        lb.place(x=10, y=90, width=176, height=190)
        return lb
    def __tk_frame_lyy7nkbb(self,parent):
        frame = Frame(parent,)
        frame.place(x=270, y=33, width=444, height=383)
        return frame
    def __tk_check_button_frameTimeline(self,parent):
        cb = Checkbutton(parent,text="Frame timeline",onvalue=1,offvalue=0,variable=self.model.enableFrameTimeline, command=self.ctl.handleEnableFrameTimeline,)
        cb.place(x=20, y=20, width=126, height=30)
        return cb
    def __tk_check_button_gameMode(self,parent):
        cb = Checkbutton(parent,text="Game intervention list(T+)",onvalue=1,offvalue=0,variable=self.model.enableGameInterventionList,command=self.ctl.handleEnableGameInterventions,)
        cb.place(x=20, y=76, width=183, height=30)
        return cb
    def __tk_check_button_networkTracing(self,parent):
        cb = Checkbutton(parent,text="Network Tracing(U+)",onvalue=1,offvalue=0,variable=self.model.enableNetworkTracing,command=self.ctl.handleEnableNetworkTracing,)
        cb.place(x=20, y=127, width=159, height=30)
        return cb
    def __tk_label_lyy7txma(self,parent):
        label = Label(parent,text="Records detailed information on network packets. Poll interval:",anchor="center", )
        label.place(x=20, y=170, width=378, height=30)
        return label
    def __tk_scale_networkTracingInterval(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=4, command=self.ctl.onSlideNetworkTracingInterval)
        scale.place(x=20, y=214, width=270, height=30)
        return scale
    def __tk_input_networkTracingInterval(self,parent):
        ipt = Entry(parent, textvariable=self.model.networkTracingInterval)
        ipt.place(x=300, y=214, width=100, height=30)
        return ipt
    def __tk_label_lyy7w4tw(self,parent):
        label = Label(parent,text="ms",anchor="center", )
        label.place(x=400, y=214, width=30, height=30)
        return label
    def __tk_check_button_callstackSampling(self,parent):
        cb = Checkbutton(parent,text="Enable callstack sampling",onvalue=1,offvalue=0,variable=self.model.enableCallstackSampling,command=self.ctl.handleEnableCallstackSampling,)
        cb.place(x=20, y=20, width=190, height=30)
        return cb
    def __tk_label_lyy80jsb(self,parent):
        label = Label(parent,text="Periodically records the current stack of processes.",anchor="center", )
        label.place(x=20, y=60, width=320, height=30)
        return label
    def __tk_label_lyy82gfv(self,parent):
        label = Label(parent,text="Sampling Frequency:",anchor="center", )
        label.place(x=20, y=100, width=138, height=30)
        return label
    def __tk_scale_callstackSamplingFreq(self,parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=0, to=9, command=self.ctl.onSlideCallstackSamplingFreq,)
        scale.place(x=20, y=140, width=340, height=30)
        return scale
    def __tk_input_callstackSamplingFreq(self,parent):
        ipt = Entry(parent, textvariable=self.model.callstackSamplingFreq,)
        ipt.place(x=390, y=140, width=100, height=30)
        return ipt
    def __tk_label_lyy84hai(self,parent):
        label = Label(parent,text="hz",anchor="center", )
        label.place(x=490, y=140, width=30, height=30)
        return label
    def __tk_label_lyy85oyw(self,parent):
        label = Label(parent,text="Filters for processes to profile, one per line:",anchor="center", )
        label.place(x=20, y=180, width=282, height=30)
        return label
    def __tk_text_callstackSamplingProcessList(self,parent):
        text = Text(parent)
        text.place(x=20, y=220, width=360, height=260)
        return text
    def __tk_label_device(self,parent):
        label = Label(parent,text="设备:",anchor="center", )
        label.place(x=24, y=10, width=50, height=30)
        return label
    def __tk_select_box_devices(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("等待设备连接...")
        cb.place(x=86, y=10, width=150, height=30)
        return cb
    def __tk_button_record(self,parent):
        btn = Button(parent, text="抓取trace", takefocus=False,)
        btn.place(x=450, y=10, width=120, height=40)
        return btn
    def __tk_button_openFileDir(self,parent):
        btn = Button(parent, text="打开trace目录", takefocus=False,)
        btn.place(x=580, y=10, width=90, height=40)
        return btn
    def __tk_button_clearTraces(self,parent):
        btn = Button(parent, text="清空历史trace", takefocus=False,)
        btn.place(x=680, y=10, width=90, height=40)
        return btn
    def __tk_select_box_configs(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("simple.config","all.config")
        cb.place(x=86, y=42, width=150, height=30)
        return cb
    def __tk_button_save_config_as(self,parent):
        btn = Button(parent, text="保存当前配置", takefocus=False,)
        btn.place(x=240, y=42, width=90, height=30)
        return btn
    def __tk_button_new_config(self,parent):
        btn = Button(parent, text="新增配置", takefocus=False,)
        btn.place(x=340, y=42, width=80, height=30)
        return btn
    def __tk_progressbar_recording(self,parent):
        progressbar = Progressbar(parent, orient=HORIZONTAL,)
        progressbar.place(x=450, y=60, width=330, height=30)
        return progressbar


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()

        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        # self.tk_list_box_kernelMeminfoCounter.bind('<<ListboxSelect>>',self.ctl.onKernelMeminfoItemSelected)
        self.tk_button_record.bind('<Button-1>',self.ctl.recordTrace)
        self.tk_button_openFileDir.bind('<Button-1>',self.ctl.openFileDiretory)
        self.tk_button_clearTraces.bind('<Button-1>',self.ctl.clearTraces)
        self.tk_button_save_config_as.bind('<Button-1>',self.ctl.saveCurrentConfig)
        self.tk_button_new_config.bind('<Button-1>',self.ctl.newConfig)
        self.tk_tabs_probes.bind("<<NotebookTabChanged>>", self.ctl.onTabChangeOfProbes)
        # 绑定鼠标事件
        self.tk_list_box_kernelMeminfoCounter.bind("<Button-1>", lambda event, listbox=self.tk_list_box_kernelMeminfoCounter: self.ctl.on_listbox_kernelmeminfo_press(listbox, event))
        self.tk_list_box_kernelMeminfoCounter.bind("<B1-Motion>", lambda event, listbox=self.tk_list_box_kernelMeminfoCounter: self.ctl.on_listbox_kernelmeminfo_drag(listbox, event))
        
        self.tk_list_box_atrace.bind("<Button-1>", lambda event, listbox=self.tk_list_box_atrace: self.ctl.on_listbox_atrace_press(listbox, event))
        self.tk_list_box_atrace.bind("<B1-Motion>", lambda event, listbox=self.tk_list_box_atrace: self.ctl.on_listbox_atrace_drag(listbox, event))

        self.tk_list_box_eventLog.bind("<Button-1>", lambda event, listbox=self.tk_list_box_eventLog: self.ctl.on_listbox_eventlog_press(listbox, event))
        self.tk_list_box_eventLog.bind("<B1-Motion>", lambda event, listbox=self.tk_list_box_eventLog: self.ctl.on_listbox_eventlog_drag(listbox, event))

        # 绑定 <<ComboboxSelected>> 事件
        self.tk_select_box_configs.bind('<<ComboboxSelected>>', self.ctl.on_trace_config_select)
        pass
    def __style_config(self):
        pass

if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
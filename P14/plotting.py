import matplotlib.pyplot as plt
import numpy as np


def plot_figure(means, stdevs, n_steps, dt, tstep=100, fbmod=None, savefig=True):
    #Plot bladder volume and bladder pressure

    # tstep (ms)
    tstop = (n_steps-1)*dt
    t = np.arange(0.0,tstop,tstep)
    ind = np.floor(t/dt).astype(np.int)
    
    timesadd = 0.5*fbmod.times[0]
    fbmod.times.insert(0,timesadd)
    fbmod.times.insert(0,0.0)
    # del fbmod.times[-1:-2]
    del fbmod.times[len(fbmod.times)-1]
    del fbmod.times[len(fbmod.times)-1]
    fbmod.times = [tx/100 for tx in fbmod.times]

    if fbmod is not None:
        fig1, ax1_1 = plt.subplots(figsize=(15,5))

        color = 'tab:red'
        ax1_1.set_xlabel('Time (t) [s]')
        ax1_1.set_xlim(left=-10,right=tstop/100+1)
        # ax1_1.set_xticks(fb)
        ax1_1.set_ylabel('Bladder Volume (V) [uL]', color=color)
        ax1_1.plot(fbmod.times, fbmod.b_vols, color=color)
        ax1_1.tick_params(axis='y', labelcolor=color)

        ax2_1 = ax1_1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2_1.set_ylabel('Bladder Pressure (P) [cmH2O]', color=color)  # we already handled the x-label with ax1
        ax2_1.set_ylim(bottom=0,top=40)
        ax2_1.plot(fbmod.times, fbmod.b_pres, color=color)
        ax2_1.tick_params(axis='y', labelcolor=color)

        fig1.tight_layout()  # otherwise the right y-label is slightly clipped

    # # tstep (ms)
    # tstop = (n_steps-1)*dt
    # t = np.arange(0.0,tstop,tstep)
    # ind = np.floor(t/dt).astype(np.int)

    fig2 = plt.figure(figsize=(15,5))
    plt.plot(t, means['Bladaff'][ind], color='b', mfc='b', mec='b', label='Bladder Afferent')
    plt.plot(t, means['PGN'][ind], color='g', mfc='g', mec='g', label='PGN')
    plt.plot(t, means['PAGaff'][ind], color='r', mfc='r', mec='r', label='Perineal Afferent')
    # plt.plot(t, means['FB'][ind], color='k', marker='D', mfc='k', mec='k', label='FB')
    plt.plot(t, means['IMG'][ind], color='y', mfc='y', mec='y', label='IMG')
    # plt.plot(t, means['IND'][ind], color='m', marker='D', mfc='m', mec='m', label='IND')

    plt.xlabel('Time (t) [s]')
    xlocs = np.arange(0.0,tstop,tstep*10)
    xlabels = [int(xl/100) for xl in xlocs]
    plt.xticks(xlocs, xlabels)
    plt.ylabel('Neuron Firing Rate (FR) [Hz]')
    plt.legend()


    # fig3 = plt.figure()
    # # plt.plot(t, means['INmminus'][ind], color='b', marker='^', mfc='b', mec='b', label='INm-')
    # # plt.plot(t, means['EUSmn'][ind], color='m', marker='^', mfc='m', mec='m', label='EUS Afferent')
    # plt.plot(t, means['IND'][ind], color='r', marker='^', mfc='r', mec='r', label='IND')
    # # plt.plot(t, means['INmplus'][ind], color='g', marker='^', mfc='g', mec='g', label='INm+')

    # plt.xlabel('Time (t) [ms]')
    # plt.ylabel('Neuron Firing Rate (FR) [Hz]')
    # plt.legend()


    if savefig:
        if fbmod is not None:
            fig1.savefig('./graphs/Pressure_vol.png',transparent=True)
        fig2.savefig('./graphs/NFR_PGN.png',transparent=True)
        # fig3.savefig('./graphs/NFR_INm.png',transparent=True)


    plt.show()

def plotting_calculator(spike_trains, n_steps, dt, window, index, num, pop):
    # window (ms)
    ind = index[pop]
    n = num[pop]
    fr_conv = np.zeros((n,n_steps))
    
    def moving_avg(x):
        window_size = np.ceil(window/dt).astype(np.int)
        x_cum = np.insert(np.cumsum(x),0,np.zeros(window_size))
        y = (x_cum[window_size:]-x_cum[:-window_size])/(window_size*dt/1000)
        return y

    for gid in range(ind,ind+n):
        spikes = np.zeros(n_steps)
        spiketimes = spike_trains.get_times(gid)
        if len(spiketimes) > 0:
            spikes[(spiketimes/dt).astype(np.int)] = 1
        fr_conv[gid-ind] = moving_avg(spikes)

    means = np.mean(fr_conv,axis=0)
    stdevs = np.std(fr_conv,axis=0)
    
    return means, stdevs
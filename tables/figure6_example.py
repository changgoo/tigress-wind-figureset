import matplotlib.pyplot as plt
import numpy as np
# Reading Tables with astropy:
from astropy.table import QTable,Table
tmean=Table.read('table-mean.ecsv')
tstd=Table.read('table-mean-err.ecsv')

# Reproducing Figure 6:

# decorating points
colors=[(0.20921568627450982, 0.45078431372549005, 0.6182352941176471),
         (0.7164705882352944, 0.7850980392156864, 0.8756862745098037),
         (0.8582352941176472, 0.5068627450980392, 0.19666666666666655),
         (0.9205882352941176, 0.733921568627451, 0.5500000000000002),
         (0.24078431372549025, 0.5592156862745098, 0.24078431372549025),
         (0.6296078431372548, 0.8245098039215686, 0.5911764705882352),
         (0.7362745098039216, 0.25588235294117645, 0.2586274509803921)]
markers=['o', 's', 'o', 's', 'o', 's', 'o']
names=['R2', 'LGR2', 'R4', 'LGR4', 'R8', 'LGR8', 'R16']

# select height where fluxes are measured
z = 'H'

# loading factors
yfields=['mass_loading','mom_kin_loading','energy_loading','metal_sn_loading']
labels=[r'$\eta_M$',r'$\eta_p^{\rm k}$',r'$\eta_E$',r'$\eta_Z^{\rm SN}$']

# SFR surface density
xfield = 'sfr40'
xlabel=r'$\Sigma_{{\rm SFR,40}}\,[M_{\odot}{\rm \, kpc^{-2}\,yr^{-1}}]$'

# set figure space
fig, axes = plt.subplots(4,2,figsize=(10,8),sharex='col',sharey='row')
_axes=axes.flatten()
iax=0

for field in yfields:
    for ph in ['cool','hot']:
        plt.sca(_axes[iax])
        for name,c,m in zip(names,colors,markers):
            idx=(tmean['phase'] == ph) & (tmean['z'] == z) & (tmean['model'] == name)
            xmean = tmean[idx][xfield]
            ymean = tmean[idx][field]
            xstd = tstd[idx][xfield]
            ystd = tstd[idx][field]
            xlogstd= xstd/xmean/np.log(10)
            ylogstd= ystd/ymean/np.log(10)
            plt.errorbar(np.log10(xmean),np.log10(ymean),
                         xerr=xlogstd,yerr=ylogstd,
                         color=c,marker=m,label=name,
                         elinewidth=2,ecolor='k',markersize=10.0,
                         markeredgecolor='k',markeredgewidth=1,
                        )
        iax += 1

# decorating axes
axes[-1,0].legend(fontsize='xx-small',ncol=4,loc='lower left')
plt.setp(axes,'xlim',(-5,0.5))
axes[0,0].set_ylim(-2,3)
axes[1,0].set_ylim(-3,1)
axes[2,0].set_ylim(-4,1)
axes[3,0].set_ylim(-4,1)
for ax,lab in zip(axes.flat,'abcdefgh'):
    ax.annotate('({})'.format(lab),[0.02,0.90],xycoords='axes fraction')

for ax,lab in zip(axes[:,0],labels):
    ax.set_ylabel(r'$\log\,$'+lab)
plt.setp(axes[-1,:],'xlabel',r'$\log\,$'+xlabel)
plt.tight_layout()
plt.show()

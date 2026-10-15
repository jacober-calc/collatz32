import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from rpn import Calc, collatz
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; PURPLE="#7048e8"; GOLD="#f2a900"; RED="#c92a2a"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white",dpi=200)
    if PREVIEW: fig.savefig(f"/tmp/cz_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def box(ax,x,y,w,h,c,lw=1.8): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.08",fc="white",ec=c,lw=lw))
def arrow(ax,a,b,c=INK,rad=0): ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=15,color=c,lw=1.6,connectionstyle=f"arc3,rad={rad}"))
def terms(n):
    c=Calc(flags={1}); c.run('Z',n); return [n]+[int(v) for _,v in c.shown]   # Flag 1 PSE values

# 1 Program flow
fig,ax=plt.subplots(figsize=(10,4.6)); ax.axis("off"); ax.set_xlim(0,10.2); ax.set_ylim(0,4.5)
ax.text(.1,4.35,"Program Flow",fontsize=13,fontweight="bold",va="center")
B=[("Z",.1,2.0,"Start","n XEQ Z\nclears, stores n",GREY),("C",2.35,2.0,"Each term","records highest,\ntests even or odd",BLUE),
   ("D",4.9,3.0,"Even","n ÷ 2",GREEN),("E",4.9,.8,"Odd","3n + 1",ORANGE),("F",7.7,3.0,"Results","Z: n  Y: highest\nX: steps",PURPLE)]
for k,x,y,t,s,c in B:
    box(ax,x,y,2.0,1.15,c); ax.text(x+1,y+.85,f"LBL {k}  {t}",ha="center",fontsize=11,fontweight="bold",color=c); ax.text(x+1,y+.3,s,ha="center",fontsize=9.5)
arrow(ax,(2.12,2.57),(2.33,2.57))
arrow(ax,(4.37,2.9),(4.88,3.4),GREEN); ax.text(4.35,3.35,"even",fontsize=9.5,color=GREEN,ha="right")
arrow(ax,(4.37,2.2),(4.88,1.5),ORANGE); ax.text(4.35,1.6,"odd",fontsize=9.5,color=ORANGE,ha="right")
arrow(ax,(6.92,3.57),(7.68,3.57),PURPLE); ax.text(7.3,3.95,"term = 1",fontsize=9.5,color=PURPLE,ha="center")
arrow(ax,(5.4,2.98),(4.37,2.75),GREEN,.0); ax.text(5.55,2.68,"term > 1",fontsize=9.5,color=GREEN)
arrow(ax,(4.9,1.4),(3.35,1.98),ORANGE,-.35)
ax.text(.1,.35,"Each new term: Flag 1 shows it for 1 second (PSE), Flag 2 stops on it (STOP; R/S continues), Σ+ counts the step",fontsize=9.5,color=GREY)
save(fig,"program_flow")

# 2 Trajectory of 27
t=terms(27); i=int(np.argmax(t))
fig,ax=plt.subplots(figsize=(10,4.4))
ax.plot(range(len(t)),t,"-o",color=BLUE,ms=3,lw=1.3)
ax.plot(i,t[i],"o",color=RED,ms=9,zorder=5); ax.annotate(f"Highest term 9,232\nat step {i}",xy=(i,t[i]),xytext=(i-45,6500),fontsize=10,color=RED,fontweight="bold",arrowprops=dict(arrowstyle="->",color=RED))
ax.plot(len(t)-1,1,"o",color=GREEN,ms=9,zorder=5); ax.text(len(t)-2,700,"1 after\n111 steps",ha="right",fontsize=10,color=GREEN,fontweight="bold")
ax.set_xlim(-2,115); ax.set_ylim(0,10200); ax.set_xlabel("Step"); ax.set_ylabel("Term")
ax.set_title("The Sequence from 27 (Example 6.2)",loc="left"); save(fig,"trajectory_27")

# 3 Steps for every starting number
N=10000; ns=np.arange(1,N+1); res=[collatz(int(n)) for n in ns]; st=np.array([r[0] for r in res]); mx=np.array([r[1] for r in res])
fig,ax=plt.subplots(figsize=(10,4.4))
ax.plot(ns,st,".",color=PURPLE,ms=1.6,alpha=.6,rasterized=True)
for n,c in ((27,RED),(6171,ORANGE)):
    ax.plot(n,st[n-1],"o",color=c,ms=8,zorder=5); ax.text(n+150,st[n-1]+6,f"{n}: {st[n-1]} steps",fontsize=10,color=c,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
ax.set_xlim(0,N); ax.set_ylim(0,280); ax.set_xlabel("Starting number n"); ax.set_ylabel("Steps to reach 1")
ax.set_title("Steps to Reach 1, n = 1 to 10,000",loc="left"); save(fig,"steps")

# 4 Highest term
fig,ax=plt.subplots(figsize=(10,4.4))
ax.plot(ns,mx,".",color=ORANGE,ms=1.6,alpha=.6,rasterized=True); ax.plot(ns,ns,color=GREY,lw=1,ls="--",label="Highest term = n")
ax.plot(27,9232,"o",color=RED,ms=8,zorder=5); ax.text(32,16000,"27: 9,232",fontsize=10,color=RED,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
k=int(np.argmax(mx)); ax.plot(k+1,mx[k],"o",color=BLUE,ms=8,zorder=5); ax.text(k+1-600,mx[k]*1.25,f"{k+1}: {mx[k]:,}",fontsize=10,color=BLUE,fontweight="bold",ha="right")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1,N); ax.set_xlabel("Starting number n"); ax.set_ylabel("Highest term")
ax.legend(frameon=False,loc="upper left",fontsize=9.5); ax.set_title("Highest Term Reached, n = 1 to 10,000",loc="left"); save(fig,"peaks")

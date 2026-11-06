"""Draw two 3D blocker examples. Run with Python + numpy/scipy/matplotlib."""
from pathlib import Path
from itertools import combinations
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

BASE = Path(__file__).resolve().parent
font = next((n for n in ['Microsoft YaHei','SimHei','SimSun']
             if any(f.name == n for f in font_manager.fontManager.ttflist)), 'DejaVu Sans')
plt.rcParams.update({'font.family':font,'axes.unicode_minus':False,
                     'font.size':13,'mathtext.fontset':'stix'})
BLUE='#437db3'; ORANGE='#ed9a29'; RED='#d55359'
LIMIT=1.4

def vertices(A,b):
    """Vertices of {x: A x >= b} in the plotting box."""
    A=np.vstack([A,np.eye(3),-np.eye(3)])
    b=np.r_[b,np.zeros(3),-LIMIT*np.ones(3)]
    found=[]
    for ids in combinations(range(len(b)),3):
        M=A[list(ids)]
        if abs(np.linalg.det(M))<1e-9: continue
        x=np.linalg.solve(M,b[list(ids)])
        if np.all(A@x>=b-1e-8) and not any(np.linalg.norm(x-v)<1e-7 for v in found):
            found.append(x)
    return np.array(found)

def poly(ax,v,color,alpha,zorder=1,skip_base=False):
    hull=ConvexHull(v)
    faces=[]; keys=set()
    for eq in hull.equations:
        key=tuple(np.round(eq,7))
        if key in keys: continue
        keys.add(key)
        pts=v[np.abs(v@eq[:3]+eq[3])<1e-7]
        if skip_base and np.allclose(pts.sum(axis=1),2): continue
        center=pts.mean(axis=0)
        u=pts[0]-center;u/=np.linalg.norm(u)
        w=np.cross(eq[:3],u)
        angles=np.arctan2((pts-center)@w,(pts-center)@u)
        faces.append(pts[np.argsort(angles)])
    ax.add_collection3d(Poly3DCollection(faces,facecolor=color,alpha=alpha,
                          edgecolor=color,linewidth=.7,zorder=zorder))

def triangle(ax,pts):
    ax.add_collection3d(Poly3DCollection([pts],facecolor=ORANGE,alpha=.75,
                                       edgecolor='#a55f08',linewidth=2,zorder=3))
    ax.scatter(*pts.T,s=38,c='#8e5004',depthshade=False,zorder=6)

def setup(ax,title):
    ax.set(xlim=(0,LIMIT),ylim=(0,LIMIT),zlim=(0,LIMIT),
           xlabel=r'$x_1$',ylabel=r'$x_2$',zlabel=r'$x_3$')
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.set_ticks([0,.5,1,1.4]);axis.pane.set_facecolor((.95,.96,.98,1))
    ax.set_box_aspect((1,1,1));ax.view_init(elev=22,azim=225)
    ax.set_title(title,pad=28,fontweight='bold',fontsize=18)
    ax.tick_params(labelsize=10)

def main():
    # Example 1: F={{1},{2},{3}}, blocker={{1,2,3}}.
    P1=np.eye(3)
    # Example 2: F=blocker={{1,2},{1,3},{2,3}}.
    P2=np.array([[1,1,0],[1,0,1],[0,1,1]],float)
    center=np.full(3,.5)
    assert np.all(P2@center>=1) and center.sum()<2
    V1=vertices(np.ones((1,3)),np.array([1.]))
    V2=vertices(np.vstack([P2,np.ones(3)]),np.array([1.,1.,1.,2.]))
    gap=np.vstack([P2,center])
    assert abs(ConvexHull(gap).volume-1/12)<1e-9

    fig=plt.figure(figsize=(15,8.8),facecolor='white')
    a=fig.add_subplot(121,projection='3d',computed_zorder=False)
    b=fig.add_subplot(122,projection='3d',computed_zorder=False)
    setup(a,'例1：LHS = RHS')
    setup(b,'例2：LHS 严格包含于 RHS')
    poly(a,V1,BLUE,.13);triangle(a,P1)
    a.text(.35,.22,.45,r'$P:\ x_1+x_2+x_3=1$',fontsize=14,zorder=10)
    a.text2D(.04,-.09,r'RHS: $x_i\geq 0,\quad x_1+x_2+x_3\geq 1$',transform=a.transAxes,fontsize=15)
    poly(b,V2,BLUE,.10);poly(b,gap,RED,.4,zorder=4,skip_base=True);triangle(b,P2)
    b.scatter(*center,s=110,c='#9d1f2d',edgecolors='white',linewidths=1,depthshade=False,zorder=8)
    b.text(.43,.43,.31,r'$q=(\frac{1}{2},\frac{1}{2},\frac{1}{2})$',fontsize=15,color='#991f2c',zorder=10)
    b.text2D(.19,.90,r'$P:\ x_1+x_2+x_3=2$',transform=b.transAxes,fontsize=14)
    b.text2D(.02,-.09,r'RHS: $x_i\geq0,\quad x_1+x_2,\ x_1+x_3,\ x_2+x_3\geq1$',transform=b.transAxes,fontsize=14)
    fig.legend(handles=[Patch(facecolor=ORANGE,edgecolor='#a55f08',label='橙色三角形：P'),
                        Patch(facecolor=BLUE,alpha=.25,label='蓝色区域：LHS（图中截取部分）'),
                        Patch(facecolor=RED,alpha=.5,label='红色四面体内部：RHS 有而 LHS 没有')],
               loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.085),fontsize=12)
    fig.text(.5,.025,'两图只显示立方体 [0, 1.4]³ 内的部分；实际区域向坐标增大的方向无界延伸。',
             ha='center',fontsize=12,color='#555555')
    fig.subplots_adjust(left=.02,right=.97,bottom=.24,top=.88,wspace=.1)
    fig.savefig(BASE/'阻塞杂族_LHS与RHS_三维示例.png',dpi=180)
    plt.close(fig)

if __name__=='__main__':main()

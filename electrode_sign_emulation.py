import os
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import plotext as plt_txt

# pyeit == 1.2.2
import numpy as np
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.eit.protocol import create

path = "plt.jpg"


def compute_electrode_signals(mesh_obj, n_el=16, el_dist=8, SNR=None):

    EIT_protocol = create(n_el=n_el, dist_exc=el_dist)
    fwd = EITForward(mesh_obj, EIT_protocol)
    v = fwd.solve_eit(mesh_obj.perm)

    if SNR is None:
        electrode_signals = v
    else:
        sigma_n2 = np.var(f.v) * 10 ** (SNR / 10)
        n = np.sqrt(sigma_n2) * np.random.normal(size=f.v.shape)
        electrode_signals = v + n

    return electrode_signals


def plot_mesh(mesh_obj, el_pos):

    pts = mesh_obj.node
    tri = mesh_obj.element
    x, y = pts[:, 0], pts[:, 1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.tripcolor(
        x,
        y,
        tri,
        np.real(mesh_obj.perm),
        edgecolors="k",
        shading="flat",
        alpha=1,
        cmap=plt.cm.viridis,
    )
    # draw electrodes
    ax.plot(x[el_pos], y[el_pos], "ro")
    for i, e in enumerate(el_pos):
        ax.text(x[e], y[e], str(i + 1), size=12)
    ax.set_title(r"mesh")
    ax.set_aspect("equal")
    ax.set_ylim([-1.2, 1.2])
    ax.set_xlim([-1.2, 1.2])
    plt.colorbar(im)
    fig.set_size_inches(6, 6)
    plt.tight_layout()
    plt.savefig(path)


print("Insert path from the first line of the new terminal:")
serial_send = input("N PTY is /dev/pts/")
print("Insert path from the second line of the new terminal:")
serial_read = input("N PTY is /dev/pts/")

ds = input("Do you want a live view of the byte data-stream? [y/n]:")

if str(ds) == "y":
    cmd = "gnome-terminal -- sh -c 'bash -c \"cat </dev/pts/{0:1}; exec bash\"'".format(
        serial_read
    )
    os.system(cmd)


send_adr = "/dev/pts/{0:1}".format(serial_send)
ser = serial.Serial(send_adr, 9600)


# h0 = mesh refinemend
empty_mesh_obj = mesh.create(h0=0.05)

while True:
    x, y = np.random.uniform(low=(-0.4, -0.4), high=(0.4, 0.4), size=2)

    mesh_obj = mesh.set_perm(
        empty_mesh_obj,
        mesh.wrapper.PyEITAnomaly_Circle(center=[x, y], perm=0.9, r=0.2),
        background=0.2,
    )

    ar = compute_electrode_signals(mesh_obj, n_el=16, el_dist=8)

    plot_mesh(mesh_obj, np.arange(16))
    plt_txt.image_plot(os.path.abspath(path))
    plt_txt.show()
    plt_txt.delete_file(os.path.abspath(path))

    # print(ar)
    barr = bytearray(ar)
    ser.write(ar)
    time.sleep(1)

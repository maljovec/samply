"""
    A flask application for visualizing the results of a 2D neighborhood
    graph
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import json
import time
import samply

app = Flask(__name__)
# ######################################################################
# Constants
D = 2
# ######################################################################
# User-editable parameters
N = 10
seed = 0
s_type = "directional"
# ######################################################################
# Dynamically computed constants
X = np.zeros((N, D))
# ######################################################################


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sample", methods=["POST"])
def makeData():
    if request.method == "POST":
        start = time.time()
        params = request.get_json()
        print(params)

        N = int(params["count"])
        seed = int(params["seed"])
        s_type = params["s_type"].strip().lower()

        np.random.seed(seed)
        if s_type == "uniform":
            X = samply.hypercube.uniform(N, D)
        elif s_type == "normal":
            X = samply.hypercube.normal(N, D)
        elif s_type == "grid":
            X = samply.hypercube.grid(N, D)
        elif s_type == "cvt":
            X = samply.hypercube.cvt(N, D)
        elif s_type == "lhs":
            X = samply.hypercube.lhs(N, D)
        elif s_type == "shell":
            X = samply.shape.shell(N, D)
        elif s_type == "dshell":
            X = samply.shape.concentric_shells(N, D, gap_ratio=0.8)
        elif s_type == "x":
            X = samply.shape.cross(N, D)
        elif s_type == "s":
            X = samply.shape.curve(N, D)
        elif s_type == "stripes":
            X = samply.shape.stripes(N, D)
        elif s_type == "distinct_mixture":
            means = [0.25 * np.ones(D), 0.5 * np.ones(D), 0.75 * np.ones(D),]
            covs = [0.00125 * np.eye(D)] * 3
            X = samply.hypercube.multimodal(N, D, means, covs)
        elif s_type == "overlap_mixture":
            X = samply.hypercube.multimodal(N, D)
        elif s_type == "halton":
            X = samply.hypercube.halton(N, D, seed)

        end = time.time()
        return jsonify(
            {
                "data": json.dumps(X.tolist(), separators=(",", ":")),
                "time": "{:6.4f} s".format(end - start),
            }
        )


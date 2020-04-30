from app import app
from flask import render_template, flash, redirect

from .forms import AnalyzeForm
import .scripts/tw

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="About")

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    form = AnalyzeForm()
    if form.validate_on_submit():
        flash("Analysis requested on handle {}".format(
            form.handle.data))
        tw.get_tweets(handle)
        return redirect("/index")
    return render_template("analyze.html", title="Analyze", form=form)

@app.route("/proposal")
def proposal():
    return render_template("proposal.html", title="Proposal")

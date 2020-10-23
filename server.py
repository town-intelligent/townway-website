from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aboutUs")
def aboutUs():
    name = request.args.get("name")

    if name == "aboutBeYoungGarden":
        return render_template("aboutBeYoungGarden.html")
    elif name == "aboutIceRoom":
        return render_template("aboutIceRoom.html")
    elif name == "aboutSkyYard":
        return render_template("aboutSkyYard.html")
    elif name == "aboutDigitalTownee":
        return render_template("aboutDigitalTownee.html")
    elif name == "aboutAsiaCreation":
        return render_template("aboutAsiaCreation.html")
    else:
        return render_template("aboutUs.html")

@app.route("/goodIdea")
def goodIdea():
    name = request.args.get("name")
    
    if name == "goodIdeaWork":
        return render_template("goodIdeaWork.html")
    elif name == "goodIdeaWork":
        return render_template("goodIdeaWork.html")
    elif name == "goodIdeaInternship":
        return render_template("goodIdeaInternship.html")
    elif name == "goodIdeaOverseas":
        return render_template("goodIdeaOverseas.html")
    else:
        return render_template("goodIdea.html")

@app.route("/store")
def store():
    return render_template("store.html")

@app.route("/latestNews")
def latestNews():
    return render_template("latestNews.html")

@app.route("/contactUs")
def contactUs():
    return render_template("contactUs.html")

# Smart shop module - start
@app.route("/organicCrops")
def organicCrops():
    page = request.args.get("page")

    if page == "organicCropsMembers":
        return render_template("organicCropsMembers.html")
    elif page == "organicCropsProduct":
        return render_template("organicCropsProduct.html")
    else:
        return render_template("organicCrops.html")

@app.route("/purchase_01")
def purchase_01():
    return render_template("purchase_01.html")

@app.route("/purchaseOrderCheck_01")
def purchaseOrderCheck_01():
    return render_template("purchaseOrderCheck_01.html")

@app.route("/purchase_02")
def purchase_02():
    return render_template("purchase_02.html")

# Smart shop module - end

if __name__ == '__main__':
    app.run(debug = True, threaded = True, host = "0.0.0.0", port = 5004)

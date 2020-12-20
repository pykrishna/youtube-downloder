from pytube import YouTube
from flask import Flask,redirect, url_for,render_template,request
import requests, random
requests.packages.urllib3.disable_warnings()
import ssl

app=Flask(__name__)

yt= None
rng = None
list1 = None
video = None

def fetch(url):
    global yt
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    try:
        yt = YouTube(url)
    except Exception as e:
        print(e)
        return -1
    else:
        return yt.streams.all()

@app.route('/')
def renderHomePage():
    return render_template("index.html")



@app.route('/work', methods=['POST','GET'])
def work():
    global list1
    global rng
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        url_dw= yout = request.form['url']
        # y = url_dw.split('/')[-1]
        # yout = f"https://www.youtube.com/watch?v={y}"

        if yout:
            # import pdb;pdb.set_trace()
            list1=fetch(yout)
            
            # import pdb;pdb.set_trace()
            if list1 == -1:
                return render_template('index.html', eval=1)

            p=len(list1)
            rng=[]
            for k in range(p):
                rng.append(k)
            return render_template('download.html', packet=zip(list1,rng))
        else:
            return render_template('index.html',eval=1)


@app.route('/success')
def success():
    global video
    render_template('success.html')
    video.download("F:/Pytube downloads/")
    return redirect(url_for('renderHomePage'))


@app.route('/receive', methods=['POST','GET'])
def receive():
    global list1
    global video
    global rng
    global yt
    try:
        choice = int(request.form['category'])
        # import pdb;pdb.set_trace()
    except Exception:
        return render_template('download.html',packet=zip(list1,rng),eval=1)
    else:
        video=list1[choice]
        try:

            save_at=request.form['save_at']
            if save_at=='':
                return render_template('download.html',packet=zip(list1,rng),eval=2)
            file =f"C:\\Users\\{save_at}\\Downloads"
            # import pdb;pdb.set_trace()
            video.download(file)

        except Exception:
            num=str(random.randrange(1,10))
            nm=video.filename
            name=nm+num
            yt.set_filename(name)
            video.download(save_at)
            return render_template('success.html',vid=video,path=save_at)
        else:
            return render_template('success.html', vid=video,path=save_at)

if __name__== '__main__':
    app.run(debug=1)

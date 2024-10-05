from flask import Flask,render_template,request,flash,redirect
import os,cv2
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key= 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename,operation):
    print(f"The operation is {operation} and file name is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    newFilename ='none'
    match operation:
          case "cgray": 
              imgprocessed =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
              newFilename =f"static/{filename}"
              cv2.imwrite(f"static/{filename}",imgprocessed)
          case "cjpg": 
              newFilename= f"static/{filename.split('.')[0]}.jpg"
              cv2.imwrite( newFilename,img)
          case "cjpeg": 
              newFilename= f"static/{filename.split('.')[0]}.jpeg"
              cv2.imwrite( newFilename,img)
          case "cpng": 
              newFilename= f"static/{filename.split('.')[0]}.png"
              cv2.imwrite( newFilename,img)
          case "reduce-half":
            height, width = img.shape[:2]
            new_size = (width // 2, height // 2)
            img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)    
            newFilename = f"static/{filename.split('.')[0]}_resized.jpg"
            cv2.imwrite(newFilename, img_resized)
          case "compress-90":
            newFilename = f"static/{filename.split('.')[0]}_compressed.png"   
            compression_quality = 90
            cv2.imwrite(newFilename, img, [cv2.IMWRITE_JPEG_QUALITY, compression_quality])
          case "compress-70":
            newFilename = f"static/{filename.split('.')[0]}_compressed.jpg"   
            compression_quality = 70 
            cv2.imwrite(newFilename, img, [cv2.IMWRITE_JPEG_QUALITY, compression_quality])
          case "compress-50":
            newFilename = f"static/{filename.split('.')[0]}_compressed.jpg"   
            compression_quality = 50 
            cv2.imwrite(newFilename, img, [cv2.IMWRITE_JPEG_QUALITY, compression_quality])
          case "compress-30":
            newFilename = f"static/{filename.split('.')[0]}_compressed.jpg"   
            compression_quality = 30
            cv2.imwrite(newFilename, img, [cv2.IMWRITE_JPEG_QUALITY, compression_quality])
            
    return newFilename
        


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit",methods = ["GET","POST"])
def edit():
    if request.method == "POST":
            if request.method == 'POST':
                operation =request.form.get("operation")
            # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return "error"
                file = request.files['file']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return "File not selected "
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new = processImage(filename,operation)
                    flash(f"Your image has been processed, your image can be downloaded <a href='/{new}' download='{new}' target='_blank'>here</a>")
                    return render_template("index.html")
    

app.run(debug=True)
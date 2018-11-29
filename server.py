import os
import boto3
import botocore
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("S3_KEY"),
    aws_secret_access_key=os.environ.get("S3_SECRET")
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("img")
        s3.upload_fileobj(
            file,
            "py-me",
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        return f"http://py-me.s3.amazonaws.com/{file.filename}"
    except Exception as e:
        print("Something Happened: ", e)
        return e

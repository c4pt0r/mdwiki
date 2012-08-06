#!/usr/bin/env python

import os
import sys    
import json
import time 
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

WIKI_PATH = os.path.abspath(os.path.dirname(__name__)) + '/wiki/'

def check_or_create_dir(path_name):
    if os.path.exists(path_name):
        return path_name

    os.makedirs(path_name)
    return path_name

#user operations
def get_members():
    filename = check_or_create_dir(WIKI_PATH) + '.users.json'
    
    usrs = []
    if os.path.exists(filename):
        with open(filename, 'r') as fp:
            usrs = json.loads(fp.read())
    return usrs

def auth(uname, pwd):
    usrs = get_members()
    return [uname, pwd] in usrs

def register(uname, pwd):
    filename = check_or_create_dir(WIKI_PATH) + '.users.json'
    usrs = []
    try:
        with open(filename, 'r') as fp:
            usrs = json.loads(fp.read())
    except:
        pass

    if uname not in [u[0] for u in usrs]:
        usrs.append((uname, pwd))
        with open(filename, 'w') as fp:
            fp.write(json.dumps(usrs))
            return True
    return False 

def get_page_content(page, version = -1):
    content = {
        'content':'',
        'editor':'',
        'date': ''
    }
    filename = check_or_create_dir(WIKI_PATH + page) + '/' + 'data.json'
    if os.path.exists(filename):
        with open(filename) as fp:
            content_list = json.loads(fp.read())
            if version == -1:
                content = content_list[-1]
            else:
                if version > len(content_list):
                    version = len(content_list) - 1
                content = content_list[version]
            return content, True
    return content, False

def edit(page, content, editor = 'sysop'):
    obj = {
        'content' : content,
        'editor' : editor,
        'date' : time.strftime('%Y-%m-%d %H:%M:%S')
    }

    filename = check_or_create_dir(WIKI_PATH + page) + '/' + 'data.json'
    content_list = []
    try:
        with open(filename) as fp:
            content_list = json.loads(fp.read())
    except:
        pass

    content_list.append(obj)
    with open(filename, 'w') as fp:
        fp.write(json.dumps(content_list))
        return True

    return False

################## page handlers ###################

@app.route('/')
def index(): return redirect('/wiki/index')
@app.route('/wiki/')
def wikiindex(): return redirect('/wiki/index')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        msg = request.args.get('msg','')
        return render_template('login.html', msg=msg)
    else:
        uname = request.form.get('uname','')
        pwd = request.form.get('pwd','')
        if auth(uname, pwd):
            session['username'] = uname
            return redirect('/')
        return redirect('/login?msg=password error')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        msg = request.args.get('msg','')
        return render_template('register.html', msg = msg)
    else:
        uname = request.form.get('uname','')
        pwd = request.form.get('pwd','')
        if register(uname, pwd):
            session['username'] = uname
            return redirect( 'wiki/')
        else:
            return redirect( 'register?msg=user already exists')

@app.route('/members')
def members_page():
    members = [i[0] for i in get_members()]
    return render_template('members.html', members = members)


@app.route('/wiki/<path:page>', methods=['GET'])
def wiki_page(page):
    version = int(request.args.get('ver', '-1'))
    content, is_exists = get_page_content(page,version)
    usr = session.get('username', None)
    return render_template('page.html', path = page,  content = content, is_exists = is_exists, usr=usr)


@app.route('/edit/<path:page>', methods=['GET', 'POST'])
def edit_page(page):
    usr = session.get('username', None)
    if usr == None:
        return redirect( '/login')
    if request.method == 'GET':
        version = int(request.args.get('ver', '-1'))
        content, _ = get_page_content(page, version) 

        usr = session.get('username', None)
        return render_template('edit.html', path = page, content = content, usr=usr)

    # post to edit page
    else:
        content = request.form.get('content','')
        edit(page, content)
        return redirect( 'wiki/' + page)


if __name__ == '__main__':
    app.secret_key = 'S3cr31k37'
    app.debug = True
    app.run(host="0.0.0.0")
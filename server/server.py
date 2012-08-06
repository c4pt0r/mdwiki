#!/usr/bin/env python

import os
import sys
import json
import time

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

WIKI_PATH = os.path.abspath(os.path.dirname(__name__)) + '/wiki/'

def check_or_create_dir(path_name):
	if os.path.exists(path_name):
		return path_name

	os.makedirs(path_name)
	return path_name


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

@app.route('/')
def index(): return redirect('/wiki/index')
@app.route('/wiki/')
def wikiindex(): return redirect('/wiki/index')


@app.route('/wiki/<path:page>', methods=['GET'])
def wiki_page(page):
	version = int(request.args.get('ver', '-1'))
	content, is_exists = get_page_content(page,version)
	return render_template('page.html', path = page,  content = content, is_exists = is_exists)


@app.route('/edit/<path:page>', methods=['GET', 'POST'])
def edit_page(page):
	if request.method == 'GET':
		version = int(request.args.get('ver', '-1'))
		content, _ = get_page_content(page, version) 
		return render_template('edit.html', path = page, content = content)

	# post to edit page
	else:
		content = request.form.get('content','')
		edit(page, content)

		return redirect( 'wiki/' + page)


if __name__ == '__main__':
	app.debug = True
	app.run()
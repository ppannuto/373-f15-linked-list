#!/usr/bin/env python3

import csv
import os
import smtplib

try:
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.mime.base import MIMEBase
except ImportError:
	from email.MIMEText import MIMEText
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEBase import MIMEBase

import sh
from sh import wget, git, rm, make, cp, diff

# n.b. newer sh will support this directly when released
class pushd(object):
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.cwd = os.getcwd()
		os.chdir(self.path)

	def __exit__(self, exception_type, exception_val, trace):
		os.chdir(self.cwd)


print("Cloning base repo...")
rm('-rf', '373-f15-linked-list')
git('clone', 'https://github.com/eecs373-f15/373-f15-linked-list')
cp('naive.out', '373-f15-linked-list/naive.out')

print("Grabbing submissions...")
wget('https://docs.google.com/spreadsheets/d/18F8ICthJunY5VFhktLD6Rgyquf8mcMl-8s80Vr1LNvQ/export?format=csv&id=18F8ICthJunY5VFhktLD6Rgyquf8mcMl-8s80Vr1LNvQ&gid=0', '-O', 'links.csv')

def attach(msg, fname):
	f = MIMEBase('text', 'plain')
	f.set_payload(open(fname).read())
	f.add_header('Content-Disposition', 'attachment;filename='+fname)
	msg.attach(f)

header = """
<p>
This email contains the results of running your most recent submission to
the autograder. A copy of <tt>list.c</tt> as tested is attached to this email.
</p>
<p>
If you disagree with any of the results of the autograder, please let the course
staff know ASAP (reply to this email).
</p>
<hr />
"""

def send_message(uniqname, body, attach_me=None):
	msg = MIMEMultipart()
	msg['Subject'] = '[EECS 373 F15] Autograder results for Linked List'
	msg['From'] = 'ppannuto@umich.edu'
	msg['To'] = uniqname+"@umich.edu"
	msg['CC'] = 'ppannuto@umich.edu'
	msg.attach(MIMEText(header+body, 'html'))

	attach(msg, 'list.c')
	if attach_me is not None:
		attach(msg, attach_me)

	send_to = msg['To'].split(', ')
	send_to.extend(msg['CC'].split(', '))
	print(msg.as_string())
	print("\n" + "*" * 80 + "\nsending to", send_to)
	if 'y' in input("Enter 'y' to send: "):
		sm.sendmail('ppannuto@umich.edu', send_to, msg.as_string())

def perfect_grade(uniqname):
	grades.write('{},{}\n'.format(uniqname, 20))
	body = """
<p>All tests passed correctly.</p>
<p><b>Your grade for this assignment is 20/20</b></p>
"""
	send_message(uniqname, body)

def no_change(uniqname):
	grades.write('{},{}\n'.format(uniqname, 0))
	body = """
<p>Your <tt>list.c</tt> shows no change from the original implementation.</p>
<p><b>Your grade for this assignment is 0/20</b></p>
	"""
	send_message(uniqname, body, 'list.out')

def handgrade(uniqname):
	ll = (line for line in open("list.out").readlines())
	gg = (line for line in open("golden.out").readlines())

	matches = 0
	total = 0

	try:
		while True:
			g = next(gg)
			while '@@ PRINT' not in g:
				g = next(gg)
			total += 1

			l = next(ll)
			while g not in l:
				l = next(ll)

			g = next(gg)
			l = next(ll)

			if g == l:
				matches += 1
	except StopIteration:
		pass

	if matches / total > 0.5:
		grades.write('{},{}\n'.format(uniqname, 10))
		body = """
<p>Your <tt>list.c</tt> matches {}% of the expected output.</p>
<p><b>Your grade for this assignment is 10/20</b></p>
""".format(int(100*(matches/total)))
	else:
		grades.write('{},{}\n'.format(uniqname, 0))
		body = """
<p>Your <tt>list.c</tt> only matches {}% of the expected output. This is not
enough to be considered a lot of effort.</p>
<p><b>Your grade for this assignment is 0/20</b></p>
""".format(int(100*(matches/total)))

	send_message(uniqname, body, 'list.out')

def grade(uniqname, link):
	print("Grading {}".format(uniqname))
	with pushd('373-f15-linked-list'):
		wget(link, '-O', 'list.c')
		make('run')
		try:
			diff('list.out', 'golden.out')
			perfect_grade(uniqname)
		except sh.ErrorReturnCode_1:
			try:
				diff('list.out', 'naive.out')
				no_change(uniqname)
			except sh.ErrorReturnCode_1:
				handgrade(uniqname)

sm = smtplib.SMTP()
sm.connect()

grades = open('grades.csv', 'w')
grades.write('uniqname,grade\n')

with open('links.csv') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		if row[0] == 'uniqname' or row[0] == 'example':
			continue

		if len(row) == 2:
			grade(*row)


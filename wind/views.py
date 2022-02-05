# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import models
import os


# Create your views here.

@require_http_methods(["POST"])
def index(request):
    response = {}
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = models.User('', '')
    if username and password:  # 确保用户名和密码都不为空
        username = username.strip()
        try:
            user = models.User.objects.get(username=username)
        except Exception as e:
            response['msg'] = str(e)
        if user.password == password:
            response['success'] = True
            response['msg'] = 'welcome'
            response['username'] = username
        else:
            response['success'] = False
    print (response)
    print (user.password)
    print (username, password)
    return JsonResponse(response)


@require_http_methods(["POST"])
def playbook_play(request):
    response = {}
    try:
        way = request.POST.get('way')
        print(way)
        # res = os.system('ls -l {}'.format(way))
        if way == 'all_in_one':
            os.system('ansible-playbook -i /etc/ansible/hosts.hostname /etc/ansible/playbooks/all_in_one.yml > /var/log/ansible_all_in_one.log')
        else:
            os.system('ansible-playbook -i /etc/ansible/hosts.{} /etc/ansible/playbooks/{}.yml > /var/log/ansible_{}.log'.format(way, way, way))
        response['data'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['data'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def servers_put(request):
    response = {}
    servers = request.POST.get("servers")
    tag = request.POST.get('tag')
    if tag == 'ssh':
        hostsfile = '/etc/ansible/hosts.ssh'
    elif tag == 'sysopt':
        hostsfile = '/etc/ansible/hosts.sysopt'
    elif tag == 'hosts':
        hostsfile = '/etc/ansible/hosts.hosts'
    elif tag == 'jdk':
        hostsfile = '/etc/ansible/hosts.jdk'
    elif tag == 'repo':
        hostsfile = '/etc/ansible/hosts.repo'
    elif tag == 'ambari':
        hostsfile = '/etc/ansible/hosts.ambari'
    elif tag == 'ambariagent':
        hostsfile = '/etc/ansible/hosts.ambariagent'
    else:
        tag == ''
    print (hostsfile)
    print (servers, type(servers))
    l = eval(servers)
    print (l, type(l))
    os.system('echo "[all]" > {}'.format(hostsfile))
    for i in range(len(l)):
        print ('hello')
        host = '{} ansible_ssh_pass={} ansible_ssh_port={}'.format(l[i]['ip'], l[i]['password'], l[i]['port'])
        print (host)
        os.system('echo {} >> {}'.format(host, hostsfile))
    response['data'] = 0
    response
    return JsonResponse(response)


@require_http_methods(["POST"])
def hostname_put(request):
    response = {}
    try:
        hostname = request.POST.get("servers")
        print (hostname, type(hostname))
        l = eval(hostname)
        print (l, type(l))
        os.system('echo "[all]" > /etc/ansible/hosts.hostname')
        for i in range(len(l)):
            hostname = '{} ansible_ssh_pass={} ansible_ssh_port={} hostname={}'.format(l[i]['ip'], l[i]['password'], l[i]['port'], l[i]['hostname'])
            print (hostname)
            os.system('echo {} >> /etc/ansible/hosts.hostname'.format(hostname))
        response['data'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['data'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def logs_get(request):
    response = {}
    try:
        logName = request.POST.get('logName')
        # print(logName)
        rlogName = '/var/log/ansible_{}.log'.format(logName)
        log = open(rlogName).read()
        # print (rlogName)
        response['data'] = 0
        response['log'] = log

    except Exception as e:
        response['msg'] = str(e)
        response['data'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def sshvar(request):
    response = {}
    try:
        jump = request.POST.get('jump')
        print(jump)
        var = 'jump: {}'.format(jump)
        print (var)
        os.system('echo {} > /etc/ansible/roles/ssh_install_single/vars/main.yml'.format(var))
        response['data'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['data'] = 1
    return JsonResponse(response)

@require_http_methods(["POST"])
def jdkvar(request):
    response = {}
    try:
        dir = request.POST.get('dir')
        print(dir)
        var = 'dir: {}'.format(dir)
        print (var)
        os.system('echo {} > /etc/ansible/roles/jdk/vars/main.yml'.format(var))
        response['data'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['data'] = 1
    return JsonResponse(response)
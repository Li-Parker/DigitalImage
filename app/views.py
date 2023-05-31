import datetime
import os
import uuid

from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
# 引入JsonResponse模块
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from app.serializers import UserSerializer, GroupSerializer
from model.RGB2GRAY.rgb2gray import *
from .models import Users, Images


class UserViewSet(viewsets.ModelViewSet):
    """查看，编辑用户的界面"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """查看，编辑组的界面"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


"""
baseURL = http://127.0.0.1:8000/api/
"""

"""
测试
"""


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_users(request):
    try:
        obj_content = Users.objects.all().values()

        contents = list(obj_content)

        return JsonResponse({'code': 1, 'data': contents})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': 'err:' + str(e)})

    pass


"""
用户登录
login/
method:'POST'
body:{
    username:'string'
    password:'string'
    }

"""


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(userName=username)

        if user.exists():
            user = user.first()
            if user.passWord == password:
                token = uuid.uuid4()
                login_user = {
                    'id': user.id,
                    'userName': user.userName,
                    'passWord': user.passWord,
                    'imageCount': user.imageCount
                }
                request.session[str(token)] = login_user
                rest = {'token': token,
                        'username': user.userName}
                # cache.set(token, login_user, 60 * 60 * 60 * 3)
                return JsonResponse({'code': 1, 'data': rest})
            else:
                return JsonResponse({'code': 0, 'msg': 'err:密码错误'})
        else:
            return JsonResponse({'code': 0, 'msg': 'err:用户不存在'})
    else:
        return JsonResponse({'code': 0, 'msg': 'err:get方法错误'})


"""
用户注册
register/
method:'POST'
body:{
    username:'string'
    password:'string'
    }
"""


def register(request):
    # parse request data
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
    except KeyError as e:
        return JsonResponse({'code': 400, 'msg': 'Bad Request - missing parameter: {}'.format(e)}, status=400)

    # check if user already exists
    if Users.objects.filter(userName=username).first():
        return JsonResponse({'code': 409, 'msg': 'Conflict - the user already exists.'}, status=409)

    # create new user and save to database
    user = Users(userName=username, passWord=password)
    user.save()

    # return response
    return JsonResponse({'code': 0, 'msg': 'Created - new user created successfully.'}, status=201)


"""
上传图片
uploadImage/
method:'POST'
header:{
    session:'string'
    }
body:{
    Image:''
    }
"""


def uploadImage(request):
    try:
        token = request.META.get('HTTP_SESSION')
        user = request.session.get(token)
        if user is None:
            return JsonResponse({'code': -1, 'msg': '会话已过期'}, status=500)
        the_user = Users.objects.get(id=user.get('id'))
        image_num = the_user.imageCount + 1
        user_name = the_user.userName
        ext_name = request.FILES.get('Image').name.split(".")[-1]
        request.FILES.get('Image').name = user_name + '-' + str(image_num) + "." + ext_name
        new_img = Images(
            img=request.FILES.get('Image'),
            name=request.FILES.get('Image').name,
            create_time=datetime.datetime.now(),
            user=Users.objects.get(id=user.get('id'))
        )
        the_user = Users.objects.get(id=user.get('id'))
        the_user.imageCount += 1
    except KeyError as e:
        return JsonResponse({'code': 400, 'msg': 'Bad Request - missing parameter: {}'.format(e)}, status=400)
    new_img.save()
    the_user.save()
    latest = Images.objects.filter(user=Users.objects.get(id=user.get('id'))).latest('create_time')
    latest_image_id = latest.id
    return JsonResponse({'code': 0, 'msg': '上传成功！', 'imageName': str(request.FILES.get('Image').name),
                         'imageId': latest_image_id}, status=201)


"""
获取用户最近上传的一张图片
getImage/
method:'GET'
header:{
    session:'string'
    }
"""


def get_latest_image(request):
    try:
        token = request.META.get('HTTP_SESSION')
        user_tmp = request.session.get(token)
        if user_tmp is None:
            return JsonResponse({'code': -1, 'msg': '会话已过期'}, status=500)
        user = Users.objects.get(id=user_tmp.get('id'))
        latest = Images.objects.filter(user=user).latest('create_time')
        response = HttpResponse(latest.img, content_type="image/jpeg")
        response['Content-Disposition'] = 'attachment:filename="{}"'.format(latest.name)
        return response
    except Users.DoesNotExist:
        return JsonResponse({'code': 404, 'msg': 'User not found'}, status=404)
    except Images.DoesNotExist:
        return JsonResponse({'code': 404, 'msg': 'Image not found'}, status=404)


"""
获取用户信息：
getUserInfo/
method:'GET'
header:{
    session:'string'
    }
"""


def get_user_info(request):
    try:
        token = request.META.get('HTTP_SESSION')
        user = request.session.get(token)
        if user is None:
            return JsonResponse({'code': -1, 'msg': '会话已过期'}, status=500)
        return JsonResponse({'code': 0, 'msg': {'userInfo': user, 'receivedToken': token}}, status=201)
    except KeyError as e:
        return JsonResponse({'code': 400, 'msg': 'Bad Request - missing parameter: {}'.format(e)}, status=400)


"""
彩色图像转灰度图像
grayImage/
method:'GET'
header:{
    session:'string'
    }
"""


def gray_image(request):
    try:
        token = request.META.get('HTTP_SESSION')
        user = request.session.get(token)
        if user is None:
            return JsonResponse({'code': -1, 'msg': '会话已过期'}, status=500)
        the_user = Users.objects.get(id=user.get('id'))
        latest = Images.objects.filter(user=the_user).latest('create_time')
        image_name = latest.name
        root_url = os.path.abspath("./")
        input_url = os.path.join(root_url, "media", image_name).replace('\\', '/')
        output_url = os.path.join(root_url, "out/RGB2GRAY", image_name).replace('\\', '/')
        rgb2gray = RGB2GRAY(input_url, output_url)
        # rgb2gray.get_GRAY_Image()
        data = rgb2gray.get_GRAY_Image()
        return JsonResponse({'code': 0, 'msg': "操作成功", 'data': data, 'url': output_url})
    except KeyError as e:
        return JsonResponse({'code': 400, 'msg': 'Bad Request - missing parameter: {}'.format(e)}, status=400)


"""
清除session
clearSession/
method:'GET'
"""


def clear_session(request):
    """清除session"""
    request.session.clear()
    return HttpResponse("清除session成功")


"""
保存图像处理后的图片
saveImage/
method:'GET'
header:{
    session:'string'
    }
"""


def save_image(request):
    try:
        token = request.META.get('HTTP_SESSION')
        user = request.session.get(token)
        if user is None:
            return JsonResponse({'code': -1, 'msg': '会话已过期'}, status=500)
        the_user = Users.objects.get(id=user.get('id'))
        latest = Images.objects.filter(user=the_user).latest('create_time')
        image_name = latest.name
        root_url = os.path.abspath("./")
        image_absolute_url = os.path.join(root_url, "out/RGB2GRAY", image_name).replace('\\', '/')
        try:
            with open(image_absolute_url, 'rb') as f:
                img_data = f.read()
        except KeyError as e:
            return JsonResponse({'code': 400, 'msg': 'Bad Request - missing parameter: {}'.format(e)}, status=400)
        save_image_name = "save-" + image_name
        file_obj = ContentFile(img_data, name=save_image_name)
        file_obj.content_type = 'image/jpeg'
        file_obj.name = save_image_name
        new_img = Images(
            img=file_obj,
            name=save_image_name,
            create_time=datetime.datetime.now(),
            user=Users.objects.get(id=user.get('id'))
        )
    except KeyError as e:
        return JsonResponse({'code': 400, 'msg': 'Bad Request - missing parameter: {}'.format(e)}, status=400)
    new_img.save()
    return JsonResponse({'code': 0, 'msg': '保存图片成功！'}, status=201)

# 后端
## Dependencies and Installation

- Python >= 3.7 (Recommend to use [Anaconda](https://www.anaconda.com/download/#linux) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
- [PyTorch >= 1.7](https://pytorch.org/)
- open-cv
- dlib

### Installation

1. Clone repo

   ```bash
   git clone https://gitee.com/li-yingda/digital-image.git
   cd digital-image
   ```

2. Install dependent packages

   ```bash
   # Install basicsr - https://github.com/xinntao/BasicSR
   # We use BasicSR for both training and inference
   pip install basicsr
   # facexlib and gfpgan are for face enhancement
   pip install facexlib
   pip install gfpgan
   pip install open-cv
   pip install -r requirements.txt
   python setup.py develop
   pip install dlib-19.19.0-cp38-cp38-win_amd64.whl.whl
   ```

​		dlib下载:http://dlib.net/ 

3. Install models

​	所有models都已下载，若有缺失可在以下链接下载

​	链接：https://pan.baidu.com/s/1QOYM6WKcNRBxynS5XANhXg?pwd=dhgy 
​	提取码：dhgy 

#### Models

- RealESRGAN_x4plus_anime_6B, RealESRGAN_x2plus , realesr-animevideov3放置在../model/Real-ESRGAN/experiments/pretrained_models


- 风格迁移解压后将model放置在../model/StyleTransfer/model


- shape_predictor_68_face_landmarks.dat放置在../model/Face/model

#### Python Files

##### ../model/BasicImageOperation/segmentation.py

实现图片分割

##### ../model/BasicImageOperation/colorize.py

实现图片上色

##### ../model/DLImageOperation/watermark.py

实现图片去水印

##### ../model/DLImageOperation/esrgan.py

实现esrgan 类调用real-esrgan模型生成图像

##### ../model/Face/face.py

实现face类实现瘦脸函数

##### ../model/Face/eye.py

实现eye类实现大眼函数

##### ../model/StyleTransfer/style.py

实现style类实现图像风格迁移函数

##### ../model/Real-ESRGAN/

real-esrgan模型

##### ../model/Watermark-Removal-Pytorch/

watermark-removal模型



#### Inference

##### Inference real-esrgan images

```bash
url:http://127.0.0.1:8000/api/esrgan/  
method:post
```

Results are in the `./out/BasicImageOperation` folder

##### Inference style-transfer images

```bash
url:http://127.0.0.1:8000/api/style/  method:get 
param:type(0-8)
0: 康定斯基作品
1：考尔德
2：糖果风格
3：毕加索名画缪斯风格
4：马赛克
5：梵高星夜风格
6：蒙克呐喊风格
7：蒙克波浪作品风格
8：抽象画风格
```

Results are in the `./out/BasicImageOperation` folder

##### Inference face-thin images

```bash
url:http://127.0.0.1:8000/api/face/  
method:get
```

Results are in the `./out/BasicImageOperation` folder

##### Inference eye-big images

```
url:http://127.0.0.1:8000/api/eyeBig/  
method:get
```

Results are in the `./out/BasicImageOperation` folder

##### Inference colorized images

```
url:http://127.0.0.1:8000/api/colorize/  
method:get 
params: type(int type=1,2,3,4)
type=1.常规上色
type=2.颜色映射上色
type=3.均衡化上色
type=4.增强上色
```

Results are in the `./out/BasicImageOperation` folder

##### Inference segmentation images

```
url:http://127.0.0.1:8000/api/segmentation/  
method:get
params:type(int type=1,2), num(int 1<=num<=50)
type=1.常规分割
type=2.对比度增强分割
```

Results are in the `./out/BasicImageOperation` folder

##### Inference watermark-removal

```
url:http://127.0.0.1:8000/api/watermark/  
method:get
```
### 文件目录及接口

Results are in the `./out/BasicImageOperation` folder


    ├─app
    |  ├─migrations            
    |  ├─__init__.py          配置文件
    |  ├─admin.py      
    |  ├─apps.py
    |  ├─models.py            mysql数据库
    |  ├─serializers.py       
    |  ├─tests.py               
    |  ├─urls.py              接口文件
    |  ├─views.py             视图函数
    ├─media                   存放上传的图片
    ├─model                   存放模型和具体图片处理函数
    |  ├─BasicImageOperation                    存放一些基本图像处理类 
    |  ├─DLImageOperation                       存放模型处理图像的类
    |  ├─Face                                   瘦脸/大眼模型
    |  ├─pytorch-CycleGAN-and-pix2pix-master    CycleGAN模型
    |  ├─Real-ESRGAN                            ESRGAN模型
    |  ├─StyleTransfer                          风格迁移模型
    |  ├─Watermark-Removal-Pytorch              出水印模型
    |  ├─rgb2gray.py                            开发测试文件
    ├─myproject                                 自动配置文件（生成项目时自动生成）
    |  ├─setting.py                             项目配置文件
    |  ├─urls.py                                根路由
    ├─out 
    |  ├─BasicImageOperation                    存放处理后的图片
1.myproject>urls.py

    urlpatterns = [
        path("admin/", admin.site.urls),
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path("api/", include('app.urls')),
    ]
2.app>urls.py

    urlpatterns = [
                      path('users/', views.get_users),                          获取用户列表，开发测试
                      path('login/', views.login),                              用户登录
                      path('register/', views.register),                        用户注册
                      path('uploadImage/', views.uploadImage),                  上传图片
                      path('getImage/', views.get_latest_image),                获取最近上传的一张图片
                      path('getOperateImage/', views.get_latest_operate_image), 获取处理后的图片
                      path('getUserInfo/', views.get_user_info),                获取用户信息
                      path('grayImage/', views.gray_image),                     彩色图像转黑白
                      path('clearSession/', views.clear_session),               清除session/token
                      path('saveImage/', views.save_image),                     保存图片
                      path('getSavedImage/', views.get_saved_latest_image),     获取保存后的图片
                      path('cartoonImage/', views.cartoon_image),               图片卡通画
                      path('dlImageOperation/', views.DL_image_operation),      CycleGAN油画风格
                      path('esrgan/', views.Es_image_operation),                高清放大
                      path('style/', views.style_transfer),                     风格转移
                      path('colorize/', views.color_image_operation),           图片上色
                      path('segmentation/', views.segmentation_image_operation),图像分隔
                      path('face/', views.faceThin),                            瘦脸
                      path('filter/', views.filter),                            滤镜
                      path('watermark/', views.watermark_removal_operation),    去水印
                      path('handleAdjust/',views.handleAdjust),                 手动编辑图片
                      path('eyeBig/', views.eyeBig)                             大眼
                  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
### 配置
    appdirs	1.4.4	1.4.4
    blas	2.117	2.117
    blas-devel	3.9.0	3.9.0
    brotli	1.0.9	1.0.9
    brotli-bin	1.0.9	1.0.9
    bzip2	1.0.8	1.0.8
    ca-certificates	2023.5.7	2023.05.30
    charset-normalizer	3.1.0	3.1.0
    click	8.1.3	8.1.3
    colorama	0.4.6	0.4.6
    cuda-cccl	12.1.109	12.0.90
    cuda-cudart	11.8.89	
    cuda-cudart-dev	11.8.89	
    cuda-cupti	11.8.87	12.0.90
    cuda-libraries	11.8.0	
    cuda-libraries-dev	11.8.0	
    cuda-nvrtc	11.8.89	12.0.76
    cuda-nvrtc-dev	11.8.89	12.0.76
    cuda-nvtx	11.8.86	
    cuda-profiler-api	12.1.105	
    cuda-runtime	11.8.0	
    docker-pycreds	0.4.0	0.4.0
    dominate	2.8.0	2.8.0
    filelock	3.12.0	3.12.2
    freetype	2.12.1	2.12.1
    gitdb	4.0.10	4.0.10
    gitpython	3.1.31	3.1.31
    idna	3.4	3.4
    intel-openmp	2023.1.0	2023.1.0
    jinja2	3.1.2	3.1.2
    jpeg	9e	9e
    jsonpatch	1.32	1.32
    jsonpointer	2.0	2.1
    lcms2	2.15	2.15
    lerc	4.0.0	4.0.0
    libabseil	20230125.2	20230125.3
    libblas	3.9.0	3.9.0
    libbrotlicommon	1.0.9	1.0.9
    libbrotlidec	1.0.9	1.0.9
    libbrotlienc	1.0.9	1.0.9
    libcblas	3.9.0	3.9.0
    libcublas	11.11.3.6	12.0.1.189
    libcublas-dev	11.11.3.6	12.0.1.189
    libcufft	10.9.0.58	11.0.0.21
    libcufft-dev	10.9.0.58	11.0.0.21
    libcurand	10.3.2.106	10.3.1.50
    libcurand-dev	10.3.2.106	10.3.1.50
    libcusolver	11.4.1.48	11.4.2.57
    libcusolver-dev	11.4.1.48	11.4.2.57
    libcusparse	11.7.5.86	12.0.0.76
    libcusparse-dev	11.7.5.86	12.0.0.76
    libdeflate	1.17	1.18
    libffi	3.4.2	3.4.4
    liblapack	3.9.0	3.9.0
    liblapacke	3.9.0	3.9.0
    libnpp	11.8.0.86	12.0.0.30
    libnpp-dev	11.8.0.86	12.0.0.30
    libnvjpeg	11.9.0.86	
    libnvjpeg-dev	11.9.0.86	
    libpng	1.6.39	1.6.39
    libprotobuf	4.23.2	4.23.3
    libsqlite	3.40.0	3.42.0
    libtiff	4.5.0	4.5.1
    libuv	1.44.2	1.44.2
    libwebp-base	1.3.0	1.3.1
    libxcb	1.13	1.15
    libzlib	1.2.13	1.2.13
    m2w64-gcc-libgfortran	5.3.0	5.3.0
    m2w64-gcc-libs	5.3.0	5.3.0
    m2w64-gcc-libs-core	5.3.0	5.3.0
    m2w64-gmp	6.1.0	6.1.0
    m2w64-libwinpthread-git	5.0.0.4634.697f757	5.0.0.4634.697f757
    mkl	2022.1.0	2023.1.0
    mkl-devel	2022.1.0	2023.1.0
    mkl-include	2022.1.0	2023.1.0
    mpmath	1.3.0	1.3.0
    msys2-conda-epoch	20160418	20160418
    networkx	3.1	3.1
    numpy	1.24.3	1.25.0
    openjpeg	2.5.0	2.5.0
    openssl	3.1.1	3.1.1
    packaging	23.1	23.1
    pathtools	0.1.2	0.1.2
    pip	23.1.2	23.1.2
    platformdirs	3.5.3	3.8.0
    pooch	1.7.0	1.7.0
    protobuf	4.23.2	4.23.3
    psutil	5.9.5	5.9.5
    pthread-stubs	0.4	0.4
    pysocks	1.7.1	1.7.1
    python	3.8.16	3.11.4
    python_abi	3.8	3.11
    pytorch	2.0.1	2.0.1
    pytorch-cuda	11.8	11.8
    pytorch-mutex	1.0	1.0
    pyyaml	6.0	6.0
    requests	2.31.0	2.31.0
    scipy	1.10.1	1.11.1
    sentry-sdk	1.21.1	1.21.1
    setproctitle	1.3.2	1.3.2
    setuptools	67.7.2	68.0.0
    six	1.16.0	1.16.0
    smmap	3.0.5	5.0.0
    sympy	1.12	1.12
    tbb	2021.7.0	2021.9.0
    tk	8.6.12	8.6.12
    tornado	6.3.2	6.3.2
    typing-extensions	4.6.3	4.7.0
    typing_extensions	4.6.3	4.7.0
    ucrt	10.0.22621.0	10.0.22621.0
    vc	14.3	14.3
    vc14_runtime	14.34.31931	14.36.32532
    visdom	0.2.4	0.2.4
    vs2015_runtime	14.34.31931	14.36.32532
    wandb	0.15.4	0.15.4
    websocket-client	1.5.3	1.6.1
    wheel	0.40.0	0.40.0
    win_inet_pton	1.1.0	1.1.0
    xorg-libxau	1.0.11	1.0.11
    xorg-libxdmcp	1.1.3	1.1.3
    xz	5.2.6	5.4.2
    yaml	0.2.5	0.2.5
    zstd	1.5.2	1.5.5

# 前端
## 如何运行
### 前端（vue3+Axios+antDesignVue+elementUI）
#### 一、搭建vue环境
1.安装node.js
vue.js 是通过 webpack来打包，而webpack 又基于 npm, npm需要nodejs环境

2.搭建vue项目环境（npm）
使用国内镜像更快,在命令提示台输入

    npm install -g cnpm --registry=https://registry.npm.taobao.org
3.安装webpack

    npm install webpack –g
4.安装脚手架

    npm install vue-cli -g

#### 二、运行vue项目
1.下载好前端代码后，删去根目录下的package-lock.json文件和node_modules 文件
2.清除npm缓存

    npm cache clean -force
3.重新安装依赖

    npm install
4.安装antDesignVue

1）.安装脚手架工具

    npm install -g @vue/cli

或者

    yarn global add @vue/cli

2）.使用组件

    npm i --save ant-design-vue

更多使用方法请参考官网：<a href="https://www.antdv.com/docs/vue/getting-started-cn/">AntDesignVue</a>

5.安装elementUI

自动导入

    npm install -D unplugin-vue-components unplugin-auto-import
更多使用方法请参考官网：<a href="https://element-plus.gitee.io/zh-CN/guide/design.html">elementUI</a>

6.运行项目

    npm run serve

## 文件目录
    ├─.gitignore
    ├─auto-imports.d.ts
    ├─components.d.ts
    ├─index.html
    ├─LICENSE
    ├─list.txt
    ├─package-lock.json
    ├─package.json
    ├─README.md
    ├─README_EN.md
    ├─tsconfig.json
    ├─tsconfig.node.json
    ├─vite.config.ts
    ├─src
    |  ├─App.vue            
    |  ├─main.ts            配置文件
    |  ├─vite-env.d.ts      
    |  ├─views  
    |  |   ├─403.vue        显示403错误页面
    |  |   ├─404.vue        显示404错误页面
    |  |   ├─cover.vue      本项目没有使用到
    |  |   ├─dashboard.vue  更多功能页面
    |  |   ├─home.vue       home框架页面，组织页面框架布局
    |  |   ├─login.vue      封页，启动项目后进入的第一个页面，登录/注册
    |  |   ├─table.vue      一键滤镜页面
    |  |   ├─tabs.vue       编辑图片页面
    |  |   ├─transfer.vue   风格迁移页面
    |  |   ├─tmp.vue        测试页面，仅用于开发测试
    |  |   ├─user.vue       用户页面，本项目没有使用
    |  |   └web-home.vue    项目首页
    |  ├─utils
    |  |   └request.ts      公共配置文件
    |  ├─store
    |  |   ├─permiss.ts     控制不同用户访问权限，本项目未使用
    |  |   ├─sidebar.ts     
    |  |   └tags.ts         
    |  ├─router 
    |  |   └index.ts        路由配置
    |  ├─images             存放静态页面图片
    |  ├─components
    |  |     ├─header.vue   本项目未使用
    |  |     ├─sidebar.vue  顶部导航栏
    |  |     └tags.vue      标签导航，本实验未使用
    |  ├─assets             用于存放一些公共配置
    |  |   ├─img
    |  |   |  ├─img.jpg
    |  |   |  └login-bg.jpg
    |  |   ├─css            公共配置样式
    |  |   |  ├─color-dark.css
    |  |   |  ├─icon.css
    |  |   |  └main.css
    |  ├─api
    |  |  └index.ts
    ├─public                公共访问页面，本项目几乎未使用
    |   ├─table.json
    |   └template.xlsx

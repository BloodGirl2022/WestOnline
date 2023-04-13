music 是后端第一次酷我音乐作业# spring-boot-jdbc



## 运行前端项目

cd 进入到文件夹

npm install

npm run build

npm run dev

## 保存

git add .
git commit -m "你想要的提交信息"
git push -u origin main



## 文件名

* fs 是functions，放一些很简单的函数
* myjwt：放鉴权相关函数
* mysql：在运行项目的时候没有使用。是自己debug的时候，想要重新创建数据库和表，写了一个自动重新创建的程序。这样就不用手动删除创建很麻烦
* manage：文件从这里开始运行
* history，search，userr，：项目的其他文件。可能称作“蓝图”，就是放在一个文件中的话，很多很杂，于是我们分类成了不同的文件。要让他们相互可以链接，就在manage中引用他们。然后在这些文件各个都标识上他们是manage的一个子文件，也就是我们说的“蓝图”（应该）。
* 所以单独运行以上3个文件没啥卵用，因为是从manage开始运行的。

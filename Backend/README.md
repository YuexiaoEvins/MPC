# MPC项目：知否
---
## **目录结构：**

- Zhifou
   - ZhiFou
      - urls.py
      - settings.py
      - wsgi.py
   - articles
      - admin.py
      - apps.py
      - models.py
      - urls.py
      - views.py
   - user
      - admin.py
      - apps.py
      - models.py
      - urls.py
      - views.py
   - manage.py      

## 例如
mysite为项目名，polls为apps名字


    mysite/
        manage.py
        mysite/
            _init_.py
            settings.py
            urls.py
            wsgi.py
        polls/
            _init_.py
            admin.py
            migrations/
                _init_.py
                0001_initial.py
            models.py
            static/
                polls/
                    images/
                        background.gif
                    style.css
            templates/
                polls/
                    detail.html
                    index.html
                    results.html
            tests.py
            urls.py
            views.py
        templates/
            admin/
                base_site.html


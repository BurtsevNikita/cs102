from bottle import run, route, redirect, template, request
import store
import news
import bayes


@route('/news')
@route('/news/')
@route('/')
def news_list():
	rows = list(bayes.guess(store.read_all()))
	colors = {'good':'#5EFF84', 'maybe':'#FFE55E', 'never':'#FFAEAE'}
	rows.sort(key = lambda x: (x[0], x[1].title, x[1].author))
	return template('news_template', rows=rows, colors=colors)


@route('/add_label/')
def add_label():
    store.update_label(int(request.query.id), request.query.label)
    redirect('/news')

@route('/update_news')
def update_news():
    store.insert_articles(news.get_news())
    redirect('/news')


    

run(host='localhost', port=8080)



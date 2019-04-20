import redis
import copy
import asyncio
from aiohttp import ClientSession
import configparser
import json
from model.post import Post

class RequestHandler:
    """Makes async requests to the specified API endpoints"""

    def __init__(self, ini: str):
        config = configparser.ConfigParser()
        config.read(ini)
        self.API_ENDPOINT = config['DEFAULT']['api']
        self.cache = redis.Redis(config['REDIS']['hostname'],config['REDIS']['port'])
        #expirey time for cache entry
        self.time_to_expire = config['REDIS']['expiry'] #seconds
    def get_posts(self, tags):
        """Gets all unique posts that have at least one of supplied tags

        Parameters
        ----------
        tags : list(str)
            list of tags

        Returns
        -------
        List(dictionaries)
            List of posts that have at least one of the supplied tags

        """
        query_tags = copy.copy(tags)
        final_results = list()
        #caching functionality
        for tag in tags:
            cached_data = self.cache.get(tag)
            if cached_data != None:
                query_tags.remove(tag)
                final_results.append(cached_data)
        if len(query_tags) != 0:
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.get_tags(query_tags))
            results = loop.run_until_complete(future)
            #add our new results into the cache
            for index in range(len(results)):
                self.cache.set(query_tags[index], results[index], ex=self.time_to_expire)
            final_results += results
        posts = list(map(lambda x: json.loads(x), final_results))
        all_posts = []
        for post in posts:
            object_form = list( map(lambda data: Post(data), post['posts']) )
            all_posts += object_form
        all_posts = list(set( all_posts ))
        return all_posts

    def get_author_data(self):
        """Part4, retreives the author meta data
        Returns
        -------
        type
            list of dictionaries
        """
        query_data = ['authors', 'posts']
        final_results = list()
        #check if the data is cached first
        for data in ['authors', 'posts']:
            cached_data= self.cache.get(data)
            if cached_data != None:
                query_data.remove(data)
                final_results.append(cached_data)
        #still data remaining to be received from the API_ENDPOINT
        if(len(query_data) != 0):
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.get_urls(query_data))
            results = loop.run_until_complete(future)
            #cache the retreived data
            for index in range(len(results)):
                self.cache.set(query_data[index], results[index], ex=self.time_to_expire)
            final_results += results
        #print(results)
        author_data, blog_data = json.loads(final_results[0]),json.loads(final_results[1])
        return self.update_authors(author_data['authors'], blog_data['posts'])

    async def get_urls(self, urls):
        """Short summary.

        Parameters
        ----------
        urls : list(str)

        Returns
        -------
        list(str)
            The results of our HTTP GET requests to the server

        """
        tasks = []
        async with ClientSession() as session:
            for name in urls:
                url = f'{self.API_ENDPOINT}/{name}'
                #print('url: ', url)
                task = asyncio.ensure_future(self.fetch(url, session))
                tasks.append(task)
                responses = await asyncio.gather(*tasks)
            return responses

    def sort_posts(self, posts, sortBy, direction):
        order = direction == 'desc'
        if not sortBy: sortBy = 'id'
        return sorted(posts, key=lambda post: post.get_element(sortBy),reverse=order)

    def update_authors(self, author_data, post_data):
        """Updates the meta data of the author as stated in Step 4.

        Parameters
        ----------
        author_data : list(str)
        post_data : list(str)

        Returns
        -------
        list(dictionaries)
            Updated author data
        """
        authors = dict()
        #set up the authors
        for author in author_data:
            id = author['id']
            authors[id] = author
            author['tags'] = dict()
            author['posts'] = list()
            author["totalLikeCount"]=authors[id]["totalReadCount"]=0
        #update meta data
        for post in post_data:
            author = authors[post['authorId']]
            author['posts'].append(post)
            #check if tag already recorded
            for tag in post['tags']:
                if tag not in author['tags']: author['tags'][tag] = 1
            author["totalLikeCount"] += post['likes']
            author["totalReadCount"] += post['reads']
        #convert from tag dict to list
        for _,data in authors.items():
            data['tags'] = list(data['tags'].keys())
        return list(authors.values())

    async def get_tags(self, tags):
        """Async HTTP requests to retreive each tag

        Parameters
        ----------
        tags : list(str)
            list of tags

        Returns
        -------
        list(str)
            The results of our HTTP GET requests to the server
        """
        api = f'{self.API_ENDPOINT}/posts?tag='
        tasks = []
        async with ClientSession() as session:
            for tag in tags:
                    url = f'{api}{tag}'
                    task = asyncio.ensure_future(self.fetch(url, session))
                    tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return responses

    async def fetch(self, url, session):
        """Asynchronously send an HTTP GET to the target URL

        Parameters
        ----------
        url : str
        session : ClientSession
        """
        async with session.get(url) as response:
            return await response.read()

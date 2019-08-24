import os


class BooksCrawlerPipeline(object):
    def process_item(self, item, spider):
        current_dir = '/'.join(os.path.abspath('.').split('/')[:-1])
        os.chdir(os.path.join(current_dir, 'bc_images'))

        if item['images'][0]['path']:
            new_image_path = 'full/' + item['title'][0] + '.jpg'
            os.rename(item['images'][0]['path'], new_image_path)

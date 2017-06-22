import markovify
from pathlib import Path
from get_comments import get_all_posts

def create_model(user, state_size=2):
    posts = get_all_posts(user);
    text = '\n'.join([ post['text'] for post in posts])
    print('generating model...');
    return markovify.Text(text, state_size=state_size);

def get_model(user):
    saved_model = Path('./%s_model.json' % user);
    if saved_model.is_file():
        print('model exists for %s, loading...' % user);
        return markovify.Text.from_json(open('%s_model.json' % user, 'r').read());
    
    print('Creating model...');
    model = create_model(user);
    print('Writing model to disk...');
    target = open('%s_model.json' % user, 'w');
    target.write(model.to_json());
    target.close();
    return model;

def generate_sentences(user, number=5):
    model = get_model(user);
    print('Generating %d sentences' % number);
    for i in range(number):
        print(model.make_sentence());

generate_sentences(get_model('chalcedon'));


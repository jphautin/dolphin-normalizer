import glob
import os.path
from collections import defaultdict

extensions = ['iso', 'gcm']

def analyse(titles, directory):
    actions = {}
    print("analyse directory %s" % directory)
    for extension in extensions:
        game_files = glob.glob(os.path.join(directory, "**", "*.%s" % extension), recursive=True)
        print("found %i %s files" % (len(game_files), extension))
        games = defaultdict(list)
        for game_file in game_files:
            with open(game_file, "rb") as content:
                name_id = content.read(6).decode('ascii')
                relative_path = game_file[len(directory) + 1:]
                # print("%s : %30s : %s" % (name_id, title, relative_path))
                games[name_id].append(relative_path)
        for id in games:
            if len(games[id]) > 1:
                actions_for_this_game = manage_duplicates_or_series(id, games[id], titles[id], extension)
                actions.update(actions_for_this_game)
            else:
                location = games[id][0]
                normalized = normalize(titles[id], id, extension)
                # print("'%s' should be renamed to '%s'" % (location, normalized))
                actions[location] = normalized
    return actions


def normalize(name, game_id, extension, index=1):
    filename = 'game.%s' % extension if index == 1 else 'disc%i.%s' % (index, extension)
    return os.path.join("%s [%s]" % (name.replace(':', ' -'), game_id), filename)


def manage_duplicates_or_series(game_id, path_list, title, extension):
    actions = {}
    sequences = defaultdict(list)
    for path in path_list:
        file = os.path.basename(path)
        possible_index = file.rsplit('.')[-2][-1]
        if possible_index in ['1', '2', '3']:
            sequences[possible_index].append(path)
        else:
            sequences[1].append(path)
    duplicates = False
    for index in sequences:
        duplicates = duplicates or len(sequences[index]) > 1
    if duplicates:
        print("WARN: DUPLICATES found in %s" % path_list)
        print("WARN: No actions can be done on theses files.")
    else:
        for index in sequences:
            location = sequences[index][0]
            normalized = normalize(title, game_id, extension, int(index))
            # print("'%s' should be renamed to '%s'" % (location, normalized))
            actions[location] = normalized
    return actions

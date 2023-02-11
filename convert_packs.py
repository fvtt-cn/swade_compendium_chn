import json
import argparse
import os.path
import re
from collections import OrderedDict


encoding = 'utf-8' # used for all io operations
json_object_type = OrderedDict

def flattened_json_items(data, key_prefix=''):
    for (key, value) in data.items():
        if isinstance(value, json_object_type):
            yield from flattened_json_items(value, f'{key_prefix}{key}.')
        else:
            yield (f'{key_prefix}{key}', value)

def flattened_json(data):
    return json_object_type(flattened_json_items(data))

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def convert(compendium_file, en_comp_file, out_file, de_compendium, en_compendium, label, trans_file=None):
  target_json = json_object_type()
  entries = {}
  mapping = {
    "Talente": {
      "name": "name",
      "description": "system.description.value",
      "prerequisites": "system.prerequisites.value"
    },
    "Zauber": {
        "name": "name",
        "description": "system.description.value",
        "duration": {
          "path": "system.duration.value",
          "converter": "time"
        },
        "materials": "system.materials.value",
        "target": "system.target.value",
        "range": {
          "path": "system.range.value",
          "converter": "range"
        },
        "components": {
          "path": "system.components.value",
          "converter": "components"
        },
        "time": {
          "path": "system.time.value",
          "converter": "time"
        }
    },
    "Ausrüstung": {
      "name": "name",
      "description": "system.description.value",
      "price": {
        "path": "system.price.value",
        "converter": "coins"
      }
    }
  }
  mapping_source = {
    "Talente": {
      "name": "name",
      "description": "system.description.value",
      "prerequisites": "system.prerequisites"
    },
    "Zauber": {
      "name": "name",
      "description": "system.description.value",
      "duration": "system.duration.value",
      "materials": "system.materials.value",
      "target": "system.target.value"
    },
    "Ausrüstung": {
      "name": "name",
      "description": "system.description.value"
    }
  }
  count = 0
  err = 0
  if (trans_file):
    trans_file.write("{\n")
  trenner = ""
  names = {}
  ids = {}
  with en_comp_file as file:
    for zeile in file:
      raw_data = json.loads(zeile, object_pairs_hook=json_object_type)
      en_json = flattened_json(raw_data)
      names[en_json['name'].lower()] = en_json['_id']
      ids[en_json['_id']] = en_json['name']

  with compendium_file as file:
    for zeile in file:
      raw_data = json.loads(zeile, object_pairs_hook=json_object_type)
      source_json = flattened_json(raw_data)
      name_list = source_json['name'].split('/')
      key = name_list[0]
      if len(name_list) > 1:
        key = name_list[1]

      if key.lower() in names:
        # key (mit Name) in en_comp gefunden!
        if (trans_file):
          trans_file.write(trenner + "\"@Compendium[lang-de-pf2e." + de_compendium + "." + source_json['_id'] + "]\": \"@Compendium[pf2e." + en_compendium + "." + names[key.lower()] + "]\"")
        count += 1
        trenner = ",\n"
        entries[key] = {}
        for m in mapping_source[label]:
          if mapping_source[label][m] in source_json:
            if m == "prerequisites":
              entries[key][m] = []
              for x in source_json[mapping_source[label][m]]:
                entries[key][m].append({"value": x})
            else:
              if source_json[mapping_source[label][m]]:
                entries[key][m] = source_json[mapping_source[label][m]]
      elif 'flags.core.sourceId' in source_json:
        sourceId = source_json['flags.core.sourceId'].split('.')
        # Eintrag nach letztem Punkt ist vermutlich die ID des Originals
        key2 = sourceId[len(sourceId)-1]
        if key2 in ids:
          # ID in en_comp gefunden!
          if (trans_file):
            trans_file.write(trenner + "\"@Compendium[lang-de-pf2e." + de_compendium + "." + source_json['_id'] + "]\": \"@Compendium[pf2e." + en_compendium + "." + key2 + "]\"")
          key = ids[key2]
          # key ist nun der Englische Originalname
          count += 1
          trenner = ",\n"
          entries[key] = {}
          for m in mapping_source[label]:
            if mapping_source[label][m] in source_json:
              if m == "prerequisites":
                entries[key][m] = []
                for x in source_json[mapping_source[label][m]]:
                  entries[key][m].append({"value": x})
              else:
                if source_json[mapping_source[label][m]]:
                  entries[key][m] = source_json[mapping_source[label][m]]
        else:
          if (trans_file):
            trans_file.write(trenner + "\"@Compendium[lang-de-pf2e." + de_compendium + "." + source_json['_id'] + "]\": \"\"")
          print("ID '" + key2 + "'/Name '" + key + "' not found in english compendium.")
          err += 1
      else:
        if (trans_file):
          trans_file.write(trenner + "\"@Compendium[lang-de-pf2e." + de_compendium + "." + source_json['_id'] + "]\": \"\"")
        print("Name '" + key + "' not found in english compendium and no sourceID attribute.")
        err += 1

  if (trans_file):
    trans_file.write("\n}")
  json.dump({'label': label, 'mapping': mapping[label], 'entries': entries}, out_file,
            ensure_ascii=False,
            indent=2)
  print("Anzahl Einträge:", count)
  print("Anzahl Fehler:", err)


def rep_links(comp_file, out_file, trans_file):
  data = trans_file.read()
  trans = json.loads(data)
  with comp_file as file:
    for zeile in file:
      out_line = replace_all(zeile, trans)
      out_file.write(out_line)


def extract(comp_file, out_file, label):
  entries = {}
  mappings = {
    "default": {
      "name": {
        "path": "name",
        "converter": "dual-language-translate"
      },
      "description": "system.description.value"
    },
    "character": {
      "name": "name",
      "description": "system.description.value"
    },
    "condition": {
      "name": "name",
      "description": "system.description.value"
    },
    "journal": {
      "name": "name",
      "pages": {
        "path": "pages",
        "converter": "pages"
      }
    },
    "npc": {
      "name": {
        "path": "name",
        "converter": "dual-language-translate"
      },
      "description": "system.details.flavorText",
      "allSaves": "system.attributes.allSaves.value",
      "speed": {
        "path": "system.attributes.speed",
        "converter": "speed"
      },
      "senses": "system.traits.senses.value",
      "sidebarText": "system.details.sidebarText",
      "source": "system.details.source.value"
    },
    "feat": {
      "name": {
        "path": "name",
        "converter": "dual-language-translate"
      },
      "description": "system.description.value",
      "prerequisites": "system.prerequisites.value"
    },
    "hazard": {
      "name": {
        "path": "name",
        "converter": "dual-language-translate"
      },
      "description": "system.details.description",
      "disable": "system.details.disable",
      "reset": "system.details.reset",
      "routine": "system.details.routine",
      "diCustom": "system.traits.di.custom",
      "stealth": "system.attributes.stealth.details",
      "items": {
        "path": "items",
        "converter": "fromPack"
      },
      "tokenName": {
        "path": "prototypeToken.name",
        "converter": "name"
      },
      "source": {
            "path": "system.source.value",
            "converter": "source-translation"
        }
    },
    "rollable-table": {
      "name": "name",
      "description": "description",
      "results": {
        "path": "results",
        "converter": "tableResults"
      }
    },
    "spell": {
        "name": {
            "path": "name",
            "converter": "dual-language-translate"
        },
        "data": {
          "path": "system",
          "converter": "spell-data"
        }
    },
    "vehicle": {
      "name": {
        "path": "name",
        "converter": "dual-language-translate"
      },
      "description": "system.details.description",
      "crew": "system.details.crew",
      "pilotingCheck": "system.details.pilotingCheck",
      "speed": "system.details.speed",
      "items": {
        "path": "items",
        "converter": "fromPack"
      },
      "tokenName": {
        "path": "prototypeToken.name",
        "converter": "name"
      },
      "source": {
            "path": "system.source.value",
            "converter": "source-translation"
        }
    }
  }
  mapping = {}
  count = 0
  with comp_file as file:
    for zeile in file:
      raw_data = json.loads(zeile, object_pairs_hook=json_object_type)
      source_json = flattened_json(raw_data)
      if mapping == {}:
        if 'type' in source_json:
          typ = source_json['type']
          if typ == 'feat':
            if source_json['system.featType.value'] == 'heritage' or source_json['system.featType.value'] == 'ancestryfeature':
              typ = 'default'
        elif 'results' in source_json:
          typ = "rollable-table"
        else:
          typ = "journal"
        if typ in mappings:
          print("Mapping gefunden:", typ)
          mapping = mappings[typ]
        else:
          mapping = mappings['default']
      key = source_json['name']
      count += 1
      trenner = ",\n"
      entries[key] = {}
      for m in mapping:
        if m == 'items':
          if m in source_json:
            entries[key][m] = {}
            for x in source_json[m]:
              entries[key][m][x['name']] = {
                "name": x['name'],
                "description": x['system']['description']['value']
              }
        elif m == 'data':
          entries[key][m] = {}
          entries[key][m]['description'] = source_json['system.description.value']
          if source_json['system.materials.value'] != "":
            entries[key][m]['materials'] = source_json['system.materials.value']
          if source_json['system.target.value'] != "":
            entries[key][m]['target'] = source_json['system.target.value']
        elif m == 'results':
          if m in source_json:
            entries[key][m] = {}
            for x in source_json[m]:
              entries[key][m][str(x['range'][0])+'-'+str(x['range'][1])] = x['text']
        elif m == 'pages':
          if m in source_json:
            entries[key][m] = {}
            for x in source_json[m]:
              entries[key][m][str(x['name'])] = {}
              entries[key][m][str(x['name'])]['name'] = x['name']
              entries[key][m][str(x['name'])]['text'] = x['text']['content']
        elif type(mapping[m]) == str:
          if mapping[m] in source_json:
            if m == "prerequisites":
              entries[key][m] = []
              for x in source_json[mapping[m]]:
                entries[key][m].append(x)
            else:
              if type(mapping[m]) == str:
                if source_json[mapping[m]]:
                  entries[key][m] = source_json[mapping[m]].replace('\u001e', '').replace('\u001f', '')
          else:
            entries[key][m] = None
        elif m == 'name':
          if 'converter' in mapping[m]:
            pfad = mapping[m]['path']
            entries[key][m] = source_json[pfad]


  json.dump({'label': label, 'mapping': mapping, 'entries': entries}, out_file,
            ensure_ascii=False,
            indent=2)
  print("Anzahl Einträge:", count)

def speed(comp_file, out_file):
  count = 0
  err = 0
  with comp_file as file:
    for zeile in file:
      # raw_data = json.loads(zeile, object_pairs_hook=json_object_type)
      # source_json = flattened_json(raw_data)
      source_json = json.loads(zeile, object_pairs_hook=json_object_type)
      if source_json['type'] == "npc":
        if 'data' in source_json:
          speed_value = source_json['data']['attributes']['speed']['value']
          if type(speed_value) == str:
            entries = speed_value.split('/')
            if entries[0][-1:] == 'm' and len(entries) == 2:
              if entries[1][-3:] == 'ft.':
                wert = entries[0:-3]
                entries[1] = str(wert) + "Fuß"
              if entries[1][-2:] == 'ft':
                wert = entries[0:-2]
                entries[1] = str(wert) + "Fuß"
              source_json['data']['attributes']['speed']['value'] = entries[1] + '/' + entries[0]
              count += 1
        else:
          print(source_json['name'] + ":")
          err += 1
      json.dump(source_json, out_file, ensure_ascii=False, indent=None)
      out_file.write("\n")

  print('Anzahl konvertierter Einträge:', count)
  print('Anzahl fehlerhafter Einträge:', err)

class HelpAction(argparse._HelpAction):
    # Code from https://stackoverflow.com/a/24122778
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        print('')
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print(f'{choice} command:')
                print(subparser.format_help())
        parser.exit()


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action=HelpAction)
    parser.add_argument('comp_file',
                        type=argparse.FileType('r', encoding=encoding),
                        help='The compendium db file')

    subparsers = parser.add_subparsers(required=True,
                                       metavar='command',
                                       dest='command')

    convert_parser = subparsers.add_parser('convert',
                                          help='Convert compendium db file to Babele translation file')
    convert_parser.add_argument('-e', '--en_file',
                                type=argparse.FileType('r', encoding=encoding),
                                help='The EN compendium db file',
                                required=True)
    convert_parser.add_argument('-o', '--out_file',
                                type=argparse.FileType('w', encoding=encoding),
                                help='The output JSON translation file',
                                required=True)
    convert_parser.add_argument('--de_comp',
                                required=True)
    convert_parser.add_argument('--en_comp',
                                required=True)
    convert_parser.add_argument('-l', '--label',
                                required=True)
    convert_parser.add_argument('--trans_file',
                                type=argparse.FileType('w', encoding=encoding),
                                help='The dict file with the translation items in format   {"old": "new",...}')

    replinks_parser = subparsers.add_parser('rep_links',
                                            help='Change links in compendium')
    replinks_parser.add_argument('-o', '--out_file',
                                type=argparse.FileType('w', encoding=encoding),
                                help='The converted compendium db file',
                                required=True)
    replinks_parser.add_argument('--trans_file',
                                type=argparse.FileType('r', encoding=encoding),
                                help='The dict file with the translation items in format   "old": "new",...',
                                required=True)

    extract_parser = subparsers.add_parser('extract',
                                          help='Extract Babele translation file from english compendium db file')
    extract_parser.add_argument('-o', '--out_file',
                                type=argparse.FileType('w', encoding=encoding),
                                help='The output JSON translation file',
                                required=True)
    extract_parser.add_argument('-l', '--label',
                                required=True)

    speed_parser = subparsers.add_parser('speed',
                                          help='Convert speed in actors.db from m/ft. to ft./m')
    speed_parser.add_argument('-o', '--out_file',
                                type=argparse.FileType('w', encoding=encoding),
                                help='The output db file',
                                required=True)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.command == 'convert':
        convert(args.comp_file, args.en_file, args.out_file, args.de_comp, args.en_comp, args.label, args.trans_file)
    elif args.command == 'rep_links':
      rep_links(args.comp_file, args.out_file, args.trans_file)
    elif args.command == 'extract':
      extract(args.comp_file, args.out_file, args.label)
    elif args.command == 'speed':
      speed(args.comp_file, args.out_file)

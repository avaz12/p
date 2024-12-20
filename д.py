


from collections import Counter
import sys

def clean_text(text_list):
    letters = "йцукенгшщзхъфывапролджэячсмитьбю"
    digits = "0123456789-"
    all_signs = letters + digits + "..."
    clean_text_list = []
    
    for word in text_list:
        clean_word = "".join([i for i in word if i in all_signs])
        if len(clean_word) > 0:
            clean_text_list.append(clean_word)
    return clean_text_list

def count_words_counter(text_list):
    counter = Counter(text_list)
    return dict(counter)

def output_result(file_name, text_dict, title=""):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(title + "\n\n")
        
        # Разделяем числовые и строковые ключи
        numeric_keys = {k: v for k, v in text_dict.items() if isinstance(k, int)}
        string_keys = {k: v for k, v in text_dict.items() if isinstance(k, str)}
        
        # Сортируем и записываем числовые ключи
        for key, value in sorted(numeric_keys.items()):
            f.write(f"Длина {key}: {value}\n")
        
        # Записываем строковые ключи
        if string_keys:
            f.write("\nСтатистика по знакам препинания:\n")
            for key, value in sorted(string_keys.items()):
                f.write(f"'{key}': {value}\n")

def count_stat(text, text_dict):
    sign_list = ['.', ',', ';', '?', '!', '"', '...']
    
    # Считаем знаки препинания
    result_dict_sign = {i: text.count(i) for i in sign_list}
    
    # Считаем количество слов по длине
    max_len = max(map(lambda x: len(x), text_dict.keys()))
    result_dict = {num: sum([text_dict[i] for i in text_dict if len(i) == num]) 
                   for num in range(1, max_len + 1)}
    
    # Объединяем статистику по знакам и длинам слов
    result_dict.update(result_dict_sign)
    
    # Удаляем нулевые значения
    result_dict = {k: v for k, v in result_dict.items() if v > 0}
    
    return result_dict

if __name__ == "__main__":
    arg_list = sys.argv
    if len(arg_list) < 2:
        print("Не указан файл для парсинга.")
        sys.exit(1)
    
    file_name = arg_list[1]
    
    # Открытие файла с кодировкой cp1251 (для русского языка на Windows)
    try:
        with open(file_name, "r", encoding="cp1251") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Ошибка декодирования файла {file_name}. Проверьте кодировку.")
        sys.exit(1)
    
    text = text.lower()
    text_list = text.split()
    cleaned_text_list = clean_text(text_list)
    
    word_counter = count_words_counter(cleaned_text_list)
    output_result("word_stat.txt", word_counter, "Статистика по длине слов:")
    
    result_stat_dict = count_stat(text, word_counter)
    output_result("final_stat.txt", result_stat_dict, "Итоговая статистика:")
    
    print("Статистика сохранена в файлы 'word_stat.txt' и 'final_stat.txt'.")

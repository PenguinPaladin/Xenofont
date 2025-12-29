import aiohttp
import asyncio
import json
from typing import AsyncGenerator

async def ask_llama_stream(
    prompt: str,
    model: str = "gemma2:2b",
    max_length: int = 800
) -> AsyncGenerator[str, None]:
    """
    Улучшенный потоковый запрос с гарантированной целостностью фраз.
    """
    url = "http://192.168.1.155:11434/api/generate"

    # Добавляем инструкцию для полноты ответа
    system_prompt = "Ты - голосовой ассистент Ксенофонт. Отвечай развернуто, но законченными предложениями."
    full_prompt = f"{system_prompt}\n\nВопрос: {prompt}\nОтвет:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": True,
        "options": {
            "num_predict": max_length,
            "temperature": 0.7,
            "top_p": 0.9,
            "repeat_penalty": 1.1
        }
    }

    buffer = ""
    sentence_buffer = ""
    
    try:
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    yield f"[Ошибка API: {response.status}] {error_text[:100]}"
                    return

                async for line in response.content:
                    if line:
                        try:
                            decoded = line.decode('utf-8').strip()
                            if decoded:
                                # Обрабатываем JSON
                                if decoded.startswith('data: '):
                                    data = json.loads(decoded[6:])
                                else:
                                    data = json.loads(decoded)
                                
                                chunk = data.get("response", "")
                                
                                if chunk:
                                    buffer += chunk
                                    sentence_buffer += chunk
                                    
                                    # Ищем законченные предложения
                                    sentence_endings = ['.', '!', '?', ';']
                                    
                                    for ending in sentence_endings:
                                        if ending in sentence_buffer:
                                            # Находим последнее законченное предложение
                                            last_end = sentence_buffer.rfind(ending)
                                            if last_end != -1:
                                                # Извлекаем законченное предложение
                                                complete_sentence = sentence_buffer[:last_end + 1].strip()
                                                if complete_sentence:
                                                    yield complete_sentence
                                                    # Очищаем буфер от отданной части
                                                    sentence_buffer = sentence_buffer[last_end + 1:].lstrip()
                                                    break
                                    
                                    # Если буфер стал слишком длинным, сбрасываем часть
                                    if len(sentence_buffer) > 200:
                                        # Ищем место для разрыва (пробел или запятая)
                                        break_point = -1
                                        for i in range(150, min(200, len(sentence_buffer))):
                                            if sentence_buffer[i] in [' ', ',', '.']:
                                                break_point = i
                                                break
                                        
                                        if break_point != -1:
                                            yield sentence_buffer[:break_point + 1].strip()
                                            sentence_buffer = sentence_buffer[break_point + 1:].lstrip()
                                    
                                    # Проверяем завершение
                                    if data.get("done", False):
                                        # Отдаем остаток
                                        if sentence_buffer.strip():
                                            yield sentence_buffer.strip()
                                        break
                                    
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"[OLLAMA] Ошибка обработки чанка: {e}")
                            continue
                            
    except asyncio.TimeoutError:
        yield "[Таймаут: запрос занял слишком много времени]"
    except Exception as e:
        print(f"[OLLAMA] Ошибка соединения: {e}")
        yield f"[Ошибка соединения: {str(e)[:50]}]"

async def ask_llama_fast(prompt: str, model: str = "gemma2:2b") -> str:
    """
    Быстрый запрос для коротких ответов.
    """
    url = "http://192.168.1.155:11434/api/generate"
    
    # Инструкция для краткости
    system_prompt = """Ты - голосовой ассистент Ксенофонт. 
    Отвечай кратко, но полно, 1-3 предложениями. 
    Не используй markdown-разметку. 
    Отвечай только на русском языке."""
    
    full_prompt = f"{system_prompt}\n\nВопрос: {prompt}\nОтвет:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_predict": 300,
            "temperature": 0.3,
            "top_p": 0.8,
            "repeat_penalty": 1.1
        }
    }
    
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = data.get("response", "Нет ответа.").strip()
                    
                    # Очищаем ответ от markdown и лишних пробелов
                    import re
                    answer = re.sub(r'\*\*(.*?)\*\*', r'\1', answer)  # Убираем **жирный**
                    answer = re.sub(r'\*(.*?)\*', r'\1', answer)      # Убираем *курсив*
                    answer = re.sub(r'`(.*?)`', r'\1', answer)        # Убираем `код`
                    answer = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', answer) # Убираем ссылки
                    answer = ' '.join(answer.split())  # Убираем лишние пробелы
                    
                    return answer
                else:
                    error_text = await response.text()
                    print(f"[OLLAMA] Ошибка {response.status}: {error_text[:100]}")
                    return f"[Ошибка API: {response.status}]"
                    
    except asyncio.TimeoutError:
        return "[Таймаут: запрос занял слишком много времени]"
    except Exception as e:
        print(f"[OLLAMA] Ошибка: {e}")
        return f"[Ошибка: {str(e)[:50]}]"

# Для обратной совместимости
ask_llama = ask_llama_fast
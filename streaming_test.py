# -*- coding: utf8 -*-
#!/usr/bin/python
# Copyright (C) 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sample that streams audio to the Google Cloud Speech API via GRPC."""

from __future__ import division

import contextlib
import re
import signal
import threading

from google.cloud.proto.speech.v1 import cloud_speech_pb2 as cloud_speech
import google.auth.credentials
from google.cloud.credentials import get_credentials
from google.cloud._helpers import make_secure_channel
from google.rpc import code_pb2
import pyaudio
from six.moves import queue
import chardet
from pyparsing import srange, Word, nums, Combine

RATE = 16000#44100#16000
CHUNK = 1024 

DEADLINE_SECS = 10# * 3 + 5
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'


def _audio_data_generator(buff):
    while True:
        chunk = buff.get()
        if not chunk:
            break
        data = [chunk]
        while True:
            try:
                data.append(buff.get(block=False))
            except queue.Empty:
                break
        yield b''.join(data)


def _fill_buffer(audio_stream, buff, chunk):
    try:
        while True:
            buff.put(audio_stream.read(chunk))
    except IOError:
        buff.put(None)


@contextlib.contextmanager
def record_audio(rate, chunk):
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1, rate=rate,
        input=True, frames_per_buffer=chunk,
    )

    buff = queue.Queue()
    fill_buffer_thread = threading.Thread(
        target=_fill_buffer, args=(audio_stream, buff, chunk))
    fill_buffer_thread.start()

    yield _audio_data_generator(buff)

    audio_stream.stop_stream()
    audio_stream.close()
    fill_buffer_thread.join()
    audio_interface.terminate()


def request_stream(data_stream, rate):
    recognition_config = cloud_speech.RecognitionConfig(
        encoding='LINEAR16',
        sample_rate_hertz=rate, 
        language_code='ko-KR'
    )
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config
    )

    yield cloud_speech.StreamingRecognizeRequest(
        streaming_config=streaming_config)

    for data in data_stream:
        yield cloud_speech.StreamingRecognizeRequest(audio_content=data)


def listen_print_loop(recognize_stream):

    print("Start..")
    for resp in recognize_stream:
        if resp.error.code != code_pb2.OK:
            raise RuntimeError('Server error: ' + resp.error.message)
        for result in resp.results:
            complete_word = ''
            print(result)
            print(result.alternatives)
            result_text = str(result.alternatives[0]).split(':')[1].split('\"')[1].strip()
             
            result_list = result_text.split("\\")
            word_list = []
            i=0
            for r in result_list:
                if r == '':
                    continue

                if i == 0:
                    first_code = bin(int(r, 8))
                    first_code = first_code[-4:]
                elif i == 1:
                    second_code = bin(int(r, 8))
                    third_code = second_code[-2:]
                    second_code = second_code[-6:-2]
                elif i == 2:
                    fourth_code = bin(int(r, 8))
                    fourth_code = fourth_code[-6:]
                i = i+1

                if i == 3:                    
                    i=0
                    word_list.append(parsing_korean(first_code, second_code, third_code, fourth_code))


            print('----------------------------------------------------------------')
    
            for cword in word_list:
                complete_word = complete_word + cword

            if complete_word[-1:] == u'역':
                complete_word = complete_word[:-1]
            
            print('End! ' + complete_word)       
            return

        if any(re.search(r'\b(exit|quit)\b', alt.transcript, re.I)
               for result in resp.results
               for alt in result.alternatives):
            print('Exiting..')
            break

def parsing_korean(c1, c2, c3, c4):
    word = '0b'+c1+c2+c3+c4
    return unichr(int(word,2))
       
def main():
    credentials = get_credentials()
    credentials = google.auth.credentials.with_scopes_if_required(
            credentials, [SPEECH_SCOPE])
    service = cloud_speech.SpeechStub(make_secure_channel(credentials, user_agent="laptop", host='speech.googleapis.com'))
    print("start recording")
    with record_audio(RATE, CHUNK) as buffered_audio_data:
        requests = request_stream(buffered_audio_data, RATE)
        recognize_stream = service.StreamingRecognize(requests)
        signal.signal(signal.SIGINT, lambda *_: recognize_stream.cancel())
        try:
            print(recognize_stream)
            listen_print_loop(recognize_stream)
            recognize_stream.cancel()
        except Exception as ex:
            print(str(ex))


if __name__ == '__main__':
    main()


import pytest
from helper.util import get_driver, sleep, get_file_script_context, stop_browser_app
from fp_browser_sdk.ext.speech_synthesis_voice import SpeechSynthesisVoice, SpeechSynthesisVoiceItem, \
    SpeechSynthesisVoiceAppendMode
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings


class TestSpeechSynthesisVoice(object):
    def setup_method(self):
        stop_browser_app()

    def get_script(self):
        """
        如果强制设重置，则只需要判断大于 0 就行了，否则需要判断大于 1
        """
        if int(self.config.get('speech-synthesis-voice.force-override')) == 1:
            script = get_file_script_context('./script/voices.js')
        else:
            script = get_file_script_context('./script/voices2.js')

        return script

    # @pytest.mark.skip()
    def test_injec_voices(self):
        """
        测试 支持的语音
        """
        settings = FPBrowserSettings()

        speech_synthesis_voice = SpeechSynthesisVoice() \
            .append_list(SpeechSynthesisVoiceItem().set_name('英语 美国').set_lang('en_US').set_is_local_service(False)) \
            .set_append_mode(SpeechSynthesisVoiceAppendMode.INSERT) \
            .set_force_override(True)

        settings.add_module(speech_synthesis_voice)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)

        self.driver = driver
        self.config = config

        script = self.get_script()
        value = self.driver.execute_script(script)
        setting_value = self.config.get('speech-synthesis-voice.json')

        print("支持的语音:", value, setting_value)
        for item in value:
            assert item["name"] == setting_value[0]['name']
            assert item["voiceURI"] == setting_value[0]['name']
            assert item["lang"] == setting_value[0]['lang']
            assert item["localService"] == (int(setting_value[0]['is_local_service']) == 1)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('force', [True, False])
    def test_force_override(self, force):
        """
        测试 是否覆盖
        """
        settings = FPBrowserSettings()

        speech_synthesis_voice = SpeechSynthesisVoice() \
            .append_list(SpeechSynthesisVoiceItem().set_name('英语 美国').set_lang('en_US').set_is_local_service(False)) \
            .set_append_mode(SpeechSynthesisVoiceAppendMode.INSERT) \
            .set_force_override(force)

        settings.add_module(speech_synthesis_voice)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)

        self.driver = driver
        self.config = config

        script = self.get_script()
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('speech-synthesis-voice.force-override')) == 1

        print("是否覆盖:", force, value, setting_value)

        if setting_value:
            assert len(value) == 1
        else:
            assert len(value) > 1

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('mode', [SpeechSynthesisVoiceAppendMode.INSERT, SpeechSynthesisVoiceAppendMode.PUSH])
    def test_append_mode(self, mode):
        """
        测试 追加方式
        """
        settings = FPBrowserSettings()

        speech_synthesis_voice = SpeechSynthesisVoice() \
            .append_list(SpeechSynthesisVoiceItem().set_name('英语 美国').set_lang('en_US').set_is_local_service(False)) \
            .set_append_mode(mode) \
            .set_force_override(False)

        settings.add_module(speech_synthesis_voice)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)

        self.driver = driver
        self.config = config

        script = self.get_script()
        value = self.driver.execute_script(script)
        setting_value = self.config.get('speech-synthesis-voice.append-mode')

        print("追加方式:", mode, value, setting_value)

        if setting_value == "insert":
            diff_value = value[0]
        else:
            diff_value = value[len(value) - 1]

        assert diff_value["name"] == self.config.get('speech-synthesis-voice.json')[0]['name']
        assert diff_value["voiceURI"] == self.config.get('speech-synthesis-voice.json')[0]['name']
        assert diff_value["lang"] == self.config.get('speech-synthesis-voice.json')[0]['lang']
        assert diff_value["localService"] == (
                int(self.config.get('speech-synthesis-voice.json')[0]['is_local_service']) == 1)

        self.driver.close()
        self.driver.quit()

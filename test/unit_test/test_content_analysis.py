from lexos.models.content_analysis_model import ContentAnalysisModel
import pandas as pd


class TestOptions(object):
    def __init__(self, dict_label=None, formula=None):
        self.label = dict_label
        self.dict_label = dict_label
        self.formula = formula


def test_add_corpus():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    assert test.corpus[0].name == "file1"
    assert test.corpus[0].label == "file1"
    assert test.corpus[0].content == "test"


def test_add_dictionary():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    assert test.dictionaries[0].name == "dict1"
    assert test.dictionaries[0].label == "dict1"
    assert test.dictionaries[0].content == ["test"]
    assert test.dictionaries[0].active


def test_delete_dictionary():
    test = ContentAnalysisModel(TestOptions(dict_label="dict1"))
    test.add_dictionary(file_name="dict1", content="test")
    assert len(test.dictionaries) == 1
    test.delete_dictionary()
    assert len(test.dictionaries) == 0


def test_toggle_dictionary():
    test = ContentAnalysisModel(TestOptions(dict_label="dict1"))
    test.add_dictionary(file_name="dict1", content="test")
    assert test.dictionaries[0].active
    test.toggle_dictionary()
    assert test.dictionaries[0].active is False
    test.toggle_dictionary()
    assert test.dictionaries[0].active


def test_get_active_dicts():
    test = ContentAnalysisModel(TestOptions(dict_label="dict1"))
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    test.toggle_dictionary()
    active = test.get_active_dicts()
    assert len(active) == 1
    assert active[0].name == "dict2"


def test_count_words():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    assert test.counters[0][0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test test test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    assert test.counters[0][0] == 3

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1", content="test, a")
    test.count_words()
    assert test.counters[0][0] == 2

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1", content="test, a, a test")
    test.count_words()
    assert test.counters[0][0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test test')
    test.add_dictionary(file_name="dict1", content="test, a, a test")
    test.count_words()
    assert test.counters[0][0] == 2

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test test a')
    test.add_dictionary(file_name="dict1", content="test, a, a test")
    test.count_words()
    assert test.counters[0][0] == 3


def test_generate_scores():
    test = ContentAnalysisModel(TestOptions(formula=""))
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores()
    assert test.scores[0] == 0.0
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test a')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == 0.5

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.test_option = TestOptions(formula="[dict1]*2")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test a')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == round(1 / 3, 3)


def test_generate_averages():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.test_option = TestOptions(formula="0")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == ['Averages', 1.0, 0.0, 1.0, 0.0]

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_corpus(file_name="file2", label='file2', content='other file')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.test_option = TestOptions(formula="0")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == ['Averages', 0.5, 0.0, 1.5, 0.0]

    test.count_words()
    test.test_option = TestOptions(formula="4*[dict1]**2")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == ['Averages', 0.5, 2.0, 1.5, 2.0]


def test_to_html():
    test = ContentAnalysisModel()
    assert test.to_html()


def test_to_data_frame():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_corpus(file_name="file2", label='file2', content='other file')
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    test.count_words()
    test.test_option = TestOptions(formula="")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert isinstance(test.to_data_frame(), type(pd.DataFrame()))


def test_is_secure():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    test.test_option = TestOptions(formula="")
    test.save_formula()
    assert test.is_secure()
    test.test_option = TestOptions(formula="[dict1][dict2]")
    test.save_formula()
    assert test.is_secure()
    test.test_option = TestOptions(
        formula="0123456789 +-*/ () sin cos tan log sqrt")
    test.save_formula()
    assert test.is_secure()
    test.test_option = TestOptions(formula="os.system()")
    test.save_formula()
    assert test.is_secure() is False


def test_detect_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    assert test.detect_active_dicts() == 2


def test_toggle_all_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    test.toggle_all_dicts()
    assert test.dictionaries[0].active is False
    assert test.dictionaries[1].active is False


def test_get_contents():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    dict_labels, active_dicts, toggle_all = test.get_contents()
    assert dict_labels == ['dict1', 'dict2']
    assert active_dicts == [True, True]
    assert toggle_all


def test_join_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test1")
    test.add_dictionary(file_name="dict2", content="test2")
    joined_dicts = test.join_active_dicts()
    assert joined_dicts[0].label == 'dict1'
    assert joined_dicts[0].content == 'test1'
    assert joined_dicts[1].label == 'dict2'
    assert joined_dicts[1].content == 'test2'


def test_save_formula():
    test = ContentAnalysisModel(TestOptions(formula="√([dict1])^([dict2])"))
    test.save_formula()
    assert test._formula == "sqrt([dict1])**([dict2])"


def test_check_formula():
    test = ContentAnalysisModel(TestOptions(formula="()sin(1)"))
    assert test.check_formula() == 0
    test.test_option = TestOptions(formula="(")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "Mismatched parenthesis<br>"
    test.test_option = TestOptions(formula="sin()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "sin takes exactly one argument (0 given)"\
                                   "<br>"
    test.test_option = TestOptions(formula="cos()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "cos takes exactly one argument (0 given)"\
                                   "<br>"
    test.test_option = TestOptions(formula="tan()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "tan takes exactly one argument (0 given)"\
                                   "<br>"
    test.test_option = TestOptions(formula="log()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "log takes exactly one argument (0 given)"\
                                   "<br>"


def test_analyze():
    test = ContentAnalysisModel()
    test.test_option = TestOptions(formula="[]")
    test.save_formula()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test2")
    assert test.analyze() == 0
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    result = test.analyze()
    assert result['result_table'] == test.to_html()
    assert result['dictionary_labels'] == ['dict1', 'dict2']
    assert result['active_dictionaries'] == [True, True]

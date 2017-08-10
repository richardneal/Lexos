from queue import Queue

from lexos.helpers.error_messages import NON_POSITIVE_SEGMENT_MESSAGE, \
    NEG_OVERLAP_LAST_PROP_MESSAGE, LARGER_SEG_SIZE_MESSAGE, \
    INVALID_CUTTING_TYPE_MESSAGE, \
    EMPTY_MILESTONE_MESSAGE
from lexos.processors.prepare.cutter import cut, cut_by_characters, \
    cut_by_words, cut_by_lines, cut_by_number, cut_by_milestone


class TestCutByCharacters:
    def test_empty_string(self):
        assert cut_by_characters(text="", seg_size=10, overlap=5,
                                 last_prop=0) == []
        assert cut_by_characters(text=" ", seg_size=100, overlap=0,
                                 last_prop=0.5) == [" "]

    def test_string_seg_size(self):
        assert cut_by_characters(text="ABABABAB", seg_size=10, overlap=0,
                                 last_prop=0) == ["ABABABAB"]
        assert cut_by_characters(text="ABABABAB", seg_size=2, overlap=0,
                                 last_prop=0) == ["AB", "AB", "AB", "AB"]
        assert cut_by_characters(text="ABABABAB", seg_size=3, overlap=0,
                                 last_prop=0) == ["ABA", "BAB", "AB"]
        assert cut_by_characters(text="A", seg_size=100, overlap=0,
                                 last_prop=5) == ["A"]

    def test_string_overlap(self):
        assert cut_by_characters(text="WORD", seg_size=2, overlap=0,
                                 last_prop=0) == ["WO", "RD"]
        assert cut_by_characters(text="ABBA", seg_size=2, overlap=1,
                                 last_prop=0) == ["AB", "BB", "BA"]
        assert cut_by_characters(text="ABCDE", seg_size=3, overlap=2,
                                 last_prop=0) == ["ABC", "BCD", "CDE"]
        assert cut_by_characters(text="ABCDEF", seg_size=4, overlap=3,
                                 last_prop=0) == ["ABCD", "BCDE", "CDEF"]

    def test_string_last_prop(self):
        assert cut_by_characters(text="ABABABABABA", seg_size=5, overlap=0,
                                 last_prop=0.2) == ["ABABA", "BABAB", "A"]
        assert cut_by_characters(text="ABABABABABA", seg_size=5, overlap=0,
                                 last_prop=0.21) == ["ABABA", "BABABA"]
        assert cut_by_characters(text="ABABABABABA", seg_size=5, overlap=0,
                                 last_prop=2) == ["ABABA", "BABABA"]
        assert cut_by_characters(text="ABCDEFGHIJKL", seg_size=3, overlap=0,
                                 last_prop=2) == ["ABC", "DEF", "GHIJKL"]

    def test_string_all_funcs(self):
        assert cut_by_characters(text="ABABABABABA", seg_size=4, overlap=1,
                                 last_prop=0.5) == \
            ["ABAB", "BABA", "ABAB", "BA"]

    def test_pre_conditions(self):
        try:
            _ = cut_by_characters(text="ABAB", seg_size=0, overlap=0,
                                  last_prop=0)
            raise AssertionError("Larger than zero error did not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE

        try:
            _ = cut_by_characters(text="ABAB", seg_size=2, overlap=-1,
                                  last_prop=0)
            raise AssertionError("None negative error did not raise")
        except AssertionError as error:
            assert str(error) == NEG_OVERLAP_LAST_PROP_MESSAGE

        try:
            _ = cut_by_characters(text="ABAB", seg_size=2, overlap=0,
                                  last_prop=-1)
            raise AssertionError("None negative error did not raise")
        except AssertionError as error:
            assert str(error) == NEG_OVERLAP_LAST_PROP_MESSAGE

        try:
            _ = cut_by_characters(text="ABAB", seg_size=2, overlap=2,
                                  last_prop=0)
            raise AssertionError("Overlap size error did not raise")
        except AssertionError as error:
            assert str(error) == LARGER_SEG_SIZE_MESSAGE


class TestCutByWords:
    def test_cut_by_words(self):
        assert cut_by_words(text=" ", seg_size=1, overlap=0,
                            last_prop=.5) == ["", " ", ""]
        assert cut_by_words(text="test test", seg_size=1, overlap=0,
                            last_prop=.5) == ["test", " ", "test"]
        assert cut_by_words(text="abc abc abc abc abc abc abc abc abc abc abc "
                                 "abc abc abc abc abc abc abc abc abc abc "
                                 "abc", seg_size=4, overlap=0, last_prop=.5)\
            == ["abc abc ", "abc abc ", "abc abc ", "abc abc ", "abc abc ",
                "abc abc ", "abc abc ", "abc abc ", "abc abc ", "abc abc ",
                "abc abc"]

    def test_cut_by_words_no_whitespace(self):
        assert cut_by_words(text="testtest", seg_size=1, overlap=0,
                            last_prop=.5) == ["testtest"]
        assert cut_by_words(text="helloworld helloworld", seg_size=1,
                            overlap=0, last_prop=.5) == [
                            "helloworld", " ", "helloworld"]

    def test_cut_by_words_overlap(self):
        assert cut_by_words(text="test test test", seg_size=2, overlap=1,
                            last_prop=.5) == ["test ", " test", "test ",
                                              " test"]

    def test_seg_size_assertion_error(self):
        try:
            _ = cut_by_words(text="test test", seg_size=1, overlap=1,
                             last_prop=.5)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == LARGER_SEG_SIZE_MESSAGE

        try:
            _ = cut_by_words(text="test test test", seg_size=1, overlap=2,
                             last_prop=.5)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == LARGER_SEG_SIZE_MESSAGE

    def test_cut_by_words_proportion(self):
        assert cut_by_words(text="test test test", seg_size=2, overlap=0,
                            last_prop=0) == ["test ", "test ", "test"]
        assert cut_by_words(text="test test test", seg_size=2, overlap=0,
                            last_prop=.5) == ["test ", "test ", "test"]
        assert cut_by_words(text="test test test", seg_size=2, overlap=0,
                            last_prop=1) == ["test ", "test test"]
        assert cut_by_words(text="test test test", seg_size=2, overlap=0,
                            last_prop=1.5) == ["test ", "test test"]
        assert cut_by_words(text="test test test", seg_size=2, overlap=0,
                            last_prop=2) == ["test ", "test test"]
        assert cut_by_words(text="test test test test", seg_size=2,
                            overlap=0, last_prop=.5) == [
            "test ", "test ", "test ", "test"]
        assert cut_by_words(text="test test test test", seg_size=2,
                            overlap=0, last_prop=1) == [
            "test ", "test ", "test test"]
        assert cut_by_words(text="test test test test test", seg_size=2,
                            overlap=0, last_prop=.5) == [
            "test ", "test ", "test ", "test ", "test"]
        assert cut_by_words(text="test test test test test", seg_size=2,
                            overlap=0, last_prop=1) == [
            "test ", "test ", "test ", "test test"]
        assert cut_by_words(text="test test test test test", seg_size=3,
                            overlap=0, last_prop=1) == [
            "test test", " test ", "test test"]

    def test_cut_by_words_zero_chunks_precondition(self):
        try:
            _ = cut_by_words(text=" ", seg_size=0, overlap=0, last_prop=.5)
            raise AssertionError("zero_division error did not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE

        try:
            _ = cut_by_words(text="test test", seg_size=0, overlap=0,
                             last_prop=.5)
            raise AssertionError("zero_division error did not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE

    def test_cut_by_words_neg_chunk_precondition(self):
        try:
            _ = cut_by_words(text="test", seg_size=-1, overlap=0,
                             last_prop=.5)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE

    def test_cut_by_words_neg_prop_precondition(self):
        try:
            _ = cut_by_words(text="test", seg_size=1, overlap=0,
                             last_prop=-1)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == NEG_OVERLAP_LAST_PROP_MESSAGE

    def test_cut_by_words_neg_overlap_precondition(self):
        try:
            _ = cut_by_words(text="test", seg_size=1, overlap=-1,
                             last_prop=.5)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == NEG_OVERLAP_LAST_PROP_MESSAGE


class TestCutByLines:
    def test_cut_by_lines_empty(self):
        assert cut_by_lines(text="", seg_size=1, overlap=0,
                            last_prop=0) == []
        assert cut_by_lines(text="\n", seg_size=1, overlap=0,
                            last_prop=0) == ["\n"]

    def test_cut_by_lines_regular(self):
        assert cut_by_lines(text="test", seg_size=100, overlap=0,
                            last_prop=0.5) == ["test"]
        assert cut_by_lines(text="test", seg_size=1,
                            overlap=0, last_prop=0) == ["test"]
        assert cut_by_lines(text="test\ntest\ntest", seg_size=2,
                            overlap=1, last_prop=0) == ["test\ntest\n",
                                                        "test\ntest"]
        assert cut_by_lines(text="test\ntest\ntest", seg_size=1,
                            overlap=0, last_prop=200) == ["test\n",
                                                          "test\ntest"]

    def test_cut_by_lines_line_ending(self):
        assert cut_by_lines(text="test\rtest", seg_size=1,
                            overlap=0, last_prop=0) == ["test\r", "test"]
        assert cut_by_lines(text="test\rtest\ntest", seg_size=1,
                            overlap=0, last_prop=0) == ["test\r",
                                                        "test\n", "test"]
        assert cut_by_lines(text="test\r\ntest\ntest", seg_size=2, overlap=1,
                            last_prop=200) == [
            "test\r\ntest\ntest\ntest"]

    def test_cut_by_lines_zero_seg_size(self):
        try:
            _ = cut_by_lines(text="", seg_size=0, overlap=0, last_prop=0)
            raise AssertionError("zero seg_size error did not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE

    def test_cut_by_lines_neg_nums(self):
        try:
            _ = cut_by_lines(text="", seg_size=1, overlap=-1, last_prop=-1)
            raise AssertionError("negative number error did not raise")
        except AssertionError as error:
            assert str(error) == NEG_OVERLAP_LAST_PROP_MESSAGE

    def test_cut_by_lines_larger_seg_size(self):
        try:
            _ = cut_by_lines(text="", seg_size=1, overlap=2, last_prop=0)
            raise AssertionError("smaller seg_size error did not raise")
        except AssertionError as error:
            assert str(error) == LARGER_SEG_SIZE_MESSAGE


class TestCutByNumbers:
    def test_cut_by_number_normal(self):
        assert cut_by_number("Text", 1) == ["Text"]
        assert cut_by_number("This text has five words", 5) == \
            ["This ", "text ", "has ", "five ", "words"]
        assert cut_by_number("Odd number of words in this text", 6) == \
            ["Odd number ", "of ", "words ", "in ", "this ", "text"]
        assert cut_by_number("Almost enough words here but not quite", 4) == \
            ["Almost enough ", "words here ", "but not ", "quite"]

    def test_cut_by_number_spacing(self):
        assert cut_by_number("Hanging space ", 2) == ["Hanging ", "space "]
        assert cut_by_number("Other  whitespace\n is\tfine!\n\n", 4) == \
            ["Other  ", "whitespace\n ", "is\t", "fine!\n\n"]
        assert cut_by_number("      <-There are six spaces here", 5) == \
            ["      <-There ", "are ", "six ", "spaces ", "here"]

    def test_cut_by_number_lines(self):
        assert cut_by_number(
            "Latinisalanguagewithnospaces\nYoumayfindthisdifficulttoread!", 2)\
            == ["Latinisalanguagewithnospaces\n",
                "Youmayfindthisdifficulttoread!"]
        assert cut_by_number("line\nline\nline\nline\nline", 2) == \
            ["line\nline\nline\n", "line\nline"]
        assert cut_by_number("Languageswithoutanyspacesmayhave\n"
                             "uneven\nchunks", 3) == \
            ["Languageswithoutanyspacesmayhave\n", "uneven\n", "chunks"]
        assert cut_by_number("RemovewhitespaceonChinese?", 3) == \
            ["RemovewhitespaceonChinese?"]
        assert cut_by_number("Ithinkthisiswhy\u3000Chinesetextcanbesplit", 2) \
            == ["Ithinkthisiswhy\u3000", "Chinesetextcanbesplit"]

    def test_cut_by_number_excess_chunks(self):
        assert cut_by_number("This text has too few words!", 10) == \
            ["This ", "text ", "has ", "too ", "few ", "words!"]
        assert cut_by_number("Safe!", 1000) == ["Safe!"]
        assert cut_by_number("", 1000000) == [""]
        assert cut_by_number("Reeeeeeeeeeeeeeeeeeeeeeeally long word", 6) == \
            ["Reeeeeeeeeeeeeeeeeeeeeeeally ", "long ", "word"]
        assert cut_by_number("\n\n\n\n\nword\n\n\n\n\n", 11) == \
            ["\n\n\n\n\nword\n\n\n\n\n"]

    def test_cut_by_number_bad_math(self):
        # Divide by zero exception
        try:
            _ = cut_by_number("Danger zone!", 0)
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE
        # Invalid index exception
        try:
            _ = cut_by_number("Oh gawd...", -1)
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE


class TestCutByMileStone:
    def test_milestone_empty_text(self):
        assert cut_by_milestone(text="", milestone=" ") == [""]
        assert cut_by_milestone(text="", milestone="bobcat") == [""]

    def test_milestone_empty_milestone(self):
        try:
            _ = cut_by_milestone(text="", milestone="")
            _ = cut_by_milestone(text="The bobcat slept all day.",
                                 milestone="")
            raise AssertionError("empty milestone error does not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_MILESTONE_MESSAGE

    def test_milestone_short_word(self):
        assert cut_by_milestone(text="test\ntest", milestone="a") == [
            "test\ntest"]
        assert cut_by_milestone(text="test\ntest", milestone="t") == [
            "", "es", "\n", "es", ""]
        assert cut_by_milestone(text="ABAAB", milestone="A") \
            == ["", "B", "",  "B"]

    def test_milestone_regular(self):
        text_content = "The bobcat slept all day.."
        milestone = "bobcat"
        assert cut_by_milestone(text_content, milestone) == ["The ",
                                                             " slept all day.."
                                                             ]

    def test_milestone_no_milestone_in_text(self):
        text_content = "The bobcat slept all day."
        milestone = "am"
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_longer_than_text(self):
        text_content = "The bobcat slept all day."
        milestone = "The cute bobcat slept all day."
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_check_case_sensative(self):
        text_content = "The bobcat slept all day."
        milestone = "BOBCAT"
        assert cut_by_milestone(text_content, milestone) == ["The bobcat "
                                                             "slept all day."]

    def test_milestone_whole_text_milestone(self):
        text_content = "The bobcat slept all day."
        milestone = "The bobcat slept all day."
        assert cut_by_milestone(text_content, milestone) == ["", ""]


class TestCutterFunction:
    # this unit test DOES NOT work
    def test_cutter_blank(self):
        assert cut(text=" ", cutting_value="1", cutting_type="words",
                   overlap="0", last_prop="0") == ["", " ", ""]
        assert cut(text="\n", cutting_value="1", cutting_type="lines",
                   overlap="0", last_prop="0") == ["\n"]

    # these unit tests DO NOT work if add one
    # whitespace in the front of word, due to some unknown bug
    def test_cutter_basic(self):
        assert cut(text="test\ntest\ntest", cutting_value="1",
                   cutting_type="lines", overlap="0", last_prop="0") ==\
            ["test\n", "test\n", "test"]
        assert cut(text=" test", cutting_value="1", cutting_type="words",
                   overlap="0", last_prop="0") == [" test"]
        assert cut(text="   \ntest", cutting_value="1", cutting_type="lines",
                   overlap="0", last_prop="0") == ["   \n", "test"]
        assert cut(text=" test", cutting_value="2", cutting_type="letters",
                   overlap="0", last_prop="0") == [" t", "es", "t"]
        assert cut(text="test", cutting_value="1", cutting_type="milestone",
                   overlap="0", last_prop="0") == ["test"]
        assert cut(text="test", cutting_value="test", cutting_type="milestone",
                   overlap="0", last_prop="0") == ["", ""]
        assert cut(text="test", cutting_value="e", cutting_type="milestone",
                   overlap="0", last_prop="0") == ["t", "st"]
        assert cut(text="test\ntesttest", cutting_value="3",
                   cutting_type="number", overlap="0", last_prop="0") == [
            "test\n", "testtest"]
        assert cut(text="test test test", cutting_value="3",
                   cutting_type="number", overlap="0", last_prop="0") == [
            "test ", "test ", "test"]

    def test_cutter_type(self):
        try:
            _ = cut(text="test", cutting_value='1', cutting_type="chars",
                    overlap="0", last_prop="0") == ["test"]
            raise AssertionError("invalid cutting type error does not raise")
        except AssertionError as error:
            assert str(error) == INVALID_CUTTING_TYPE_MESSAGE

    def test_cutter_negative_numbers(self):
        try:
            _ = cut(text="test", cutting_value="0", cutting_type="words",
                    overlap="0", last_prop="0") == ["test"]
            raise AssertionError("negative number error does not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_SEGMENT_MESSAGE

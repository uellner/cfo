from django import forms


class AnswerQuizForm(forms.Form):
    def __init__(self, answers_opt, *args, **kwargs):
        super(AnswerQuizForm, self).__init__(*args, **kwargs)
        self.fields['answers'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in answers_opt if answers_opt],
            widget=forms.RadioSelect(),
            required=False
        )

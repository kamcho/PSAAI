import random
from tokenize import Comment
from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from SubjectList.models import Subject
from django.contrib.auth.mixins import UserPassesTestMixin

from Term.models import CurrentTerm, Exam, Grade, GradeModel, Terms
from django.contrib.messages import success,error
from Users.models import AcademicProfile, MyUser, StudentsFeeAccount
# Create your views here.



class AddSubjectScore(UserPassesTestMixin,TemplateView):
    template_name = 'Term/add_score.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_id = self.kwargs['class_id']
        subject_id= self.kwargs['subject']
        subject = Subject.objects.get(id=subject_id)
        term = CurrentTerm.objects.all().last()
        context['term'] = term
        excluded = Exam.objects.filter(subject=subject, term=term.term).values_list('user__email')

        students = AcademicProfile.objects.filter(current_class__class_id=class_id).exclude(user__email__in=excluded)
        if not students:
            success(self.request, 'You have entered marks for all students')
        context['subject'] = subject
        context['students'] = students
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('user')
            user = MyUser.objects.get(email=email)
            score = int(request.POST.get('score'))

            try:
                grading = GradeModel.objects.filter(upper_limit__gte=score, lower_limit__lte=score).first()
                term = CurrentTerm.objects.all().last()
                subject = self.get_context_data().get('subject')
                exam = Exam.objects.create(user=user, subject=subject, score=score, comments=grading.comments , term=term.term)
                success = (self.request, f'Succesfully added marks for {user}. score = {score}')
                request.session['exclude'] = email
            except Exception as e:
                error(request, str(e))

        return redirect(request.get_full_path())
    
    def test_func(self):
        term = CurrentTerm.objects.first()
        return term.mode and self.request.user.role in ['Teacher', 'Supervisor']



    
class TermListView(TemplateView):
    template_name = 'Term/terms_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terms = Terms.objects.all().order_by('-id')
        context['terms'] = terms

        return context
    
class TermInfo(TemplateView):
    template_name = 'Term/term_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term_id = self.kwargs['term']
        term = Terms.objects.get(id=term_id)
        context['term'] = term
        test_exam()

        return context 
    
    def post(self, request, **kwargs):
        if request.method == 'POST':
            year = request.POST.get('year')
            term_ins = request.POST.get('term')
            starts_at = request.POST.get('start')
            
            ends_at = request.POST.get('end')
            term_id = self.kwargs['term']
            term = Terms.objects.get(id=term_id)

            if 'delete' in request.POST:
                term.delete()

                return redirect('terms')
            elif 'edit' in request.POST:
                term_id = self.kwargs['term']
                term = Terms.objects.get(id=term_id)
                term.year = year
                term.term = term_ins
                term.starts_at = starts_at
                term.ends_at = ends_at
                term.save()

                return redirect(request.get_full_path())
            else:
                current_term = CurrentTerm.objects.all().delete()
                current_term = CurrentTerm.objects.create(term=term)

                return redirect(request.get_full_path())



def test_exam():

    users = MyUser.objects.filter(role='Student', academicprofile__current_class__grade=4)
    subjects = Subject.objects.filter(grade=4)
    term=Terms.objects.get(year=2024, term='Term 1')
    # for subject in subjects:
    #     for user in users:
    #         ran = random.randint(42, 100)
    #         exam = Exam.objects.create(user=user,term=term, subject=subject, score=ran)


    return None
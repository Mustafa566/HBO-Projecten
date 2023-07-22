# Generated by Django 4.0.10 on 2023-06-04 14:33
# Generated by Django 4.0.9 on 2023-06-02 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=250, verbose_name='E-mailadres')),
                ('last_name', models.CharField(max_length=250, verbose_name='Achternaam')),
                ('first_name', models.CharField(max_length=250, verbose_name='Voornaam')),
                ('is_admin', models.BooleanField(default=True, verbose_name='Is administrator')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQ',
            fields=[
                ('mc_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250, verbose_name='Vraag')),
                ('option_a', models.CharField(max_length=250, verbose_name='A')),
                ('option_b', models.CharField(max_length=250, verbose_name='B')),
                ('option_c', models.CharField(blank=True, default='', max_length=250, verbose_name='C')),
                ('option_d', models.CharField(blank=True, default='', max_length=250, verbose_name='D')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Verborgen')),
            ],
            options={
                'verbose_name': 'Meerkeuzevraag',
                'verbose_name_plural': 'Meerkeuzevragen',
            },
        ),
        migrations.CreateModel(
            name='OpenQ',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250, verbose_name='Vraag')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Verborgen')),
            ],
            options={
                'verbose_name': 'Open vraag',
                'verbose_name_plural': 'Open vragen',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('team_member_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=250, verbose_name='E-mailadres')),
                ('last_name', models.CharField(max_length=250, verbose_name='Achternaam')),
                ('first_name', models.CharField(max_length=250, verbose_name='Voornaam')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is administrator')),
            ],
            options={
                'verbose_name': 'Teamlid',
                'verbose_name_plural': 'Teamleden',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('survey_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Naam enquête')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='Toelichting')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='Anonieme respons')),
                ('date_sent', models.DateField(null=True, verbose_name='Verzonden op')),
                ('url', models.URLField(default='', unique=True)),
                ('admin', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='ccforms.administrator', verbose_name='Administrator')),
                ('mc_q', models.ManyToManyField(blank=True, to='ccforms.multiplechoiceq', verbose_name='Meerkeuzevragen')),
                ('open_q', models.ManyToManyField(blank=True, to='ccforms.openq', verbose_name='Open vragen')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('response_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('date_submitted', models.DateField(auto_now_add=True, null=True, verbose_name='Ingevuld op')),
                ('mc_answers', models.ManyToManyField(to='ccforms.multiplechoiceq', verbose_name='Meerkeuzeantwoorden')),
                ('open_answers', models.ManyToManyField(to='ccforms.openq', verbose_name='Open antwoorden')),
                ('survey', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='ccforms.survey', verbose_name='Naam enquête')),
                ('tm_email', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='ccforms.teammember', verbose_name='E-mailadres teamlid')),
            ],
        ),
    ]

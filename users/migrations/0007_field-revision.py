# Generated by Django 4.2.11 on 2024-05-15 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('users', '0007_remove_customuser_first_name_and_more'), ('users', '0008_alter_profile_contact_alter_profile_social')]

    dependencies = [
        ('skills', '0002_alter_skill_skill_wikidata_item'),
        ('users', '0006_rename_parent_region_territory_parent_territory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='contact_method',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='irc',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wiki_develop',
        ),
        migrations.AddField(
            model_name='profile',
            name='team',
            field=models.CharField(blank=True, max_length=128, verbose_name='Team'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True, default='', max_length=2000, verbose_name='Short bio'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pronoun',
            field=models.CharField(blank=True, choices=[('he-him', 'He/Him'), ('she-her', 'She/Her'), ('they-them', 'They/Them'), ('not-specified', 'Not specified'), ('other', 'Other')], max_length=20, verbose_name='Pronoun'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills_available',
            field=models.ManyToManyField(blank=True, related_name='user_available_skills', to='skills.skill', verbose_name='Available capacity'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills_known',
            field=models.ManyToManyField(blank=True, related_name='user_known_skils', to='skills.skill', verbose_name='Known capacity'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills_wanted',
            field=models.ManyToManyField(blank=True, related_name='user_desired_skils', to='skills.skill', verbose_name='Wanted capacity'),
        ),
        migrations.AddField(
            model_name='profile',
            name='contact',
            field=models.JSONField(blank=True, null=True, verbose_name='Contact methods'),
        ),
        migrations.AddField(
            model_name='profile',
            name='social',
            field=models.JSONField(blank=True, null=True, verbose_name='Social medias'),
        ),
    ]

# Generated by Django 3.2.8 on 2022-01-29 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('tauxtva', models.FloatField(db_column='tauxTVA')),
            ],
            options={
                'db_table': 'categorie',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Marque',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'marque',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'panier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=1000)),
                ('prix', models.FloatField()),
                ('qtt_stock', models.IntegerField()),
                ('descript', models.CharField(max_length=10000)),
                ('image', models.URLField(max_length=1000)),
            ],
            options={
                'db_table': 'produit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('pass_field', models.CharField(db_column='pass', max_length=100)),
                ('mail', models.EmailField(max_length=1000)),
            ],
            options={
                'db_table': 'utilisateur',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id_utilisateur', models.OneToOneField(db_column='id_utilisateur', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.utilisateur')),
            ],
            options={
                'db_table': 'commande',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EstComposeDe',
            fields=[
                ('id_produit', models.OneToOneField(db_column='id_produit', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.produit')),
                ('quantite', models.IntegerField()),
            ],
            options={
                'db_table': 'est_compose_de',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Liquide',
            fields=[
                ('id_prod', models.OneToOneField(db_column='id_prod', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.produit')),
                ('litre', models.FloatField()),
            ],
            options={
                'db_table': 'liquide',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Solide',
            fields=[
                ('id_prod', models.OneToOneField(db_column='id_prod', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.produit')),
                ('kg', models.FloatField()),
            ],
            options={
                'db_table': 'solide',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Unite',
            fields=[
                ('id_prod', models.OneToOneField(db_column='id_prod', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.produit')),
            ],
            options={
                'db_table': 'unite',
                'managed': False,
            },
        ),
    ]
# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2016 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from rest_framework import serializers

from weblate.trans.models import Project, SubProject, Translation
from weblate.lang.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    web_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta(object):
        model = Language
        fields = (
            'code', 'name', 'nplurals', 'pluralequation', 'direction',
            'web_url', 'url',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:language-detail',
                'lookup_field': 'code'
            }
        }


class ProjectSerializer(serializers.ModelSerializer):
    web_url = serializers.CharField(source='get_absolute_url', read_only=True)
    source_language = LanguageSerializer(read_only=True)

    class Meta(object):
        model = Project
        fields = (
            'name', 'slug', 'web', 'source_language', 'web_url', 'url',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:project-detail',
                'lookup_field': 'slug'
            }
        }


class ComponentSerializer(serializers.ModelSerializer):
    web_url = serializers.CharField(source='get_absolute_url', read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta(object):
        model = SubProject
        fields = (
            'id', 'name', 'slug', 'project', 'vcs', 'repo', 'git_export',
            'branch', 'filemask', 'template', 'file_format', 'license',
            'license_url', 'web_url',
        )


class TranslationSerializer(serializers.ModelSerializer):
    web_url = serializers.CharField(source='get_absolute_url', read_only=True)
    subproject = ComponentSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)

    class Meta(object):
        model = Translation
        fields = (
            'id', 'language', 'subproject', 'translated', 'fuzzy', 'total',
            'translated_words', 'fuzzy_words', 'failing_checks_words',
            'total_words', 'failing_checks', 'have_suggestion', 'have_comment',
            'language_code', 'filename', 'revision', 'web_url',
        )
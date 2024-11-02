#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path
from typing import List

import eyed3
import streamlit as st


def show_ui(files: List[Path]):
    st.header('MP3 Tag Editor')
    with st.form('Utility Script'):
        auto_track = st.form_submit_button('Set track # automatically')
        if auto_track:
            for i, f in enumerate(files):
                audio = eyed3.load(f.as_posix())
                audio.tag.track_num = i
                audio.tag.save()
                st.success(f'Successfully update {f.name}')

    for f in files:
        audio = eyed3.load(f.as_posix())
        if not audio.tag:
            continue
        with st.form(f'Tag form for {f.as_posix()}'):
            (file_name_column, title_column, album_column, artist_column,
             track_column, update_column) = st.columns(6)
            file_name_column.write(f.name)
            title = title_column.text_input(label='Title',
                                            value=audio.tag.title)
            album = album_column.text_input(label='Album',
                                            value=audio.tag.album)
            artist = artist_column.text_input(label='Artist',
                                              value=audio.tag.artist)
            track = track_column.text_input(label='Track #',
                                            value=audio.tag.track_num[0])
            updated = update_column.form_submit_button('Update')
            if updated:
                try:
                    track_num = int(track)
                except ValueError:
                    st.error(f'{track} is not a number')
                    continue
                audio.tag.title = title
                audio.tag.album = album
                audio.tag.artist = artist
                # Implicitly set album artist `artist`
                audio.tag.album_artist = artist
                audio.tag.track_num = track_num
                audio.tag.save()
                st.success(f'Successfully update {f.name}')


def main():
    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    input_path = Path(args.input)
    if input_path.is_dir():
        files = sorted(input_path.glob('**/*.mp3'))
    elif input_path.exists():
        files = [input_path]
    else:
        raise RuntimeError(f'{args.input} is not a directory or a file')
    show_ui(files)


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()

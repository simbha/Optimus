# -*- coding: utf-8 -*-
"""
Various helpers
"""
import logging, os, shutil

def init_directory(directory):
    """
    Create a new directory if it does not allready exists
    """
    logger = logging.getLogger('optimus')
    if not os.path.exists(directory):
        logger.debug('Creating directory: %s', directory)
        os.makedirs(directory)
        return True
    return False

def recursive_directories_create(project_directory, structure, dry_run=False):
    """
    Recursive directory create from a "tree list"
    
    Sample tree list : ::
    
        structure = [
            [
                'sources',
                [
                    ['js'],
                    ['css'],
                ]
            ]
        ]
    """
    logger = logging.getLogger('optimus')
    
    for item in structure:
        if len(item)>0:
            new_dir = item[0]
            path_dir = os.path.join(project_directory, new_dir)
            if not os.path.exists(path_dir):
                logger.info('* Creating new directory : %s', path_dir)
                if not dry_run:
                    os.makedirs(path_dir)
            else:
                logger.warning('* Following path allready exist : %s', path_dir)
        # Follow children directories to create them
        if len(item)>1:
            recursive_directories_create(path_dir, item[1], dry_run=dry_run)
        
    return

def synchronize_assets_sources(settings, src, dest):
    """
    For now, this is just a rmtree/copytree of the given path
    
    TODO: In future, this should be a clean synchronize, like with rsync
    
    * ``src`` arg is allways a file path assumed to be located in the 
    ``settings.SOURCES_DIR``
    * ``dst`` is a file path that will be in 
    ``settings.STATIC_DIR``.
    """
    logger = logging.getLogger('optimus')
    source = os.path.join(settings.SOURCES_DIR, src)
    if not os.path.exists(source):
        logger.warning('The given source does not exist and so can not be synchronized : %s', source)
        return
    
    destination = os.path.join(settings.STATIC_DIR, src)
    if os.path.exists(destination):
        logger.debug('Removing old asset destination: %s', destination)
        shutil.rmtree(destination)
    logger.debug('Synchronizing asset from "%s" to "%s"', source, destination)
    shutil.copytree(source, destination)

def initialize(settings):
    """
    Init the needed directory structure
    """
    init_directory(settings.STATIC_DIR)
    init_directory(settings.WEBASSETS_CACHE)

    if settings.FILES_TO_SYNC is not None:
        for item in settings.FILES_TO_SYNC:
            synchronize_assets_sources(settings, *item)

def display_settings(settings, names):
    """
    Helper to display some settings if they are setted
    """
    logger = logging.getLogger('optimus')
    for item in names:
        logger.debug(" - Settings.%s = %s", item, getattr(settings, item, 'NOT SET'))

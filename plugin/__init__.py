try:
    from .kswkip.plugin import KswKiPGenerator, KswKiPImporter

    KswKiPGenerator().register()
    # KswKiPImporter().register()

except Exception as e:
    import os
    log_file = os.path.join(os.path.dirname(__file__), 'KswKiP.log')
    with open(log_file, 'w') as f:
        f.write(repr(e))

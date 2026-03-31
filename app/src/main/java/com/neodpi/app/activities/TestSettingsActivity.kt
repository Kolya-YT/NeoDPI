package com.neodpi.app.activities

import android.os.Bundle
import android.view.MenuItem
import com.neodpi.app.R
import com.neodpi.app.fragments.DomainListsFragment
import com.neodpi.app.fragments.ProxyTestSettingsFragment

class TestSettingsActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_test_settings)

        val openFragment = intent.getStringExtra("open_fragment")

        when (openFragment) {
            "domain_lists" -> {
                supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.test_settings, DomainListsFragment())
                    .commit()
            }
            else -> {
                supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.test_settings, ProxyTestSettingsFragment())
                    .commit()
            }
        }

        supportActionBar?.setDisplayHomeAsUpEnabled(true)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean = when (item.itemId) {
        android.R.id.home -> {
            onBackPressedDispatcher.onBackPressed()
            true
        }
        else -> super.onOptionsItemSelected(item)
    }
}